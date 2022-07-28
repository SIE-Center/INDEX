# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from datetime import datetime, date
from odoo.tools.translate import _
import base64
_logger = logging.getLogger(__name__)



class ValidationLines(models.Model):
    _name = "custom.vlines"
    v_id = fields.Many2one('project.task')
    container_number = fields.Char("Nro. Container")
    eta_date = fields.Datetime(string="Fecha ETA")
    custom_category = fields.Selection(
        [('24','IMMEX 24 hrs'),('36','IMMEX 36 hrs')], 
        string="Categoría")
    etapa =fields.Selection([('0','Baja'),('1','Forwarder'),('2','Agente Aduanal'),('3','Transportista'),('4','Maniobras de Carga'),('5','Finalizada')], 
        string="Etapa")
    #Forwarder
    u_forwarder = fields.Many2one('res.users', string='Forwarder')
    vfdate =    fields.Datetime('Validación Forwarder Fecha')
    vfdocs =    fields.Boolean('Cumplimiento Documentación')
    vflete =    fields.Boolean('Cumplimiento Costo Flete Marítimo')
    #Agente Aduanal
    u_aduanal =     fields.Many2one('res.users', string='Agente Aduanal')
    vadate =        fields.Datetime('Validación Agente Aduanal Fecha')
    varevalida =    fields.Boolean('Revalidación del BL')
    vafolio =       fields.Boolean('Liberación del Folio')    
    vaprevio =      fields.Boolean('Programación del Previo')
    #Transportista
    u_transportista = fields.Many2one('res.users', string='Transportista')    
    vtdate =        fields.Datetime('Validación Transportista Fecha')
    vtplaca =       fields.Char('Nº Placa')
    vtconductor =   fields.Char('Nombre del Conductor')
    #Maniobras
    vmdate =        fields.Datetime('Validación Maniobra')
    vmaniobra =    fields.Boolean('Maniobra de Carga')   
    def val_userid(self,user_id):
        user = self.env['res.users'].browse(self._context.get('uid'))
        if user_id.id != user.id:
            raise ValidationError('Solo el usuario '+str(user_id.name)+' puede realizar esta acción')
        return self

    def baja(self):
        self.etapa = '0'
        return self


    def reset(self):
        self.vfdocs = 0
        self.vflete = 0
        self.varevalida = 0
        self.vafolio = 0
        self.vaprevio = 0
        self.vtplaca = ''
        self.vtconductor =''
        self.vmaniobra =0
        self.etapa = '1'
        return self

    def val_forwarder(self):
        """
        1.- Solo el usuario u_forwarder puede ver y autorizar group_Forwarder_auth
        2.-Valida que no hayan menos de 38 horas (o Bloquea el transporte)
        3.-Valida que haya  validado sus campos
        4.-Manda actividades al agente aduanal del la línea
        5.-Pasa de Estapa
        6.-Envía Mensaje al Histórico
        """
        dif =  self.eta_date - datetime.now()
        horas = int(dif.total_seconds()/3600)
        if horas < 38:
            self.etapa = '0'
            body = '->Hay '+str(horas)+' horas de diferencia solo se permiten diferencias mayores a  38 horas entre la la fecha actual y la estimada la línea será Bloqueada'
            self.v_id.message_post(body=body)
            return self
        self.val_userid(self.u_forwarder)
        if self.vfdocs == False or self.vflete == False:
            raise ValidationError('Debe Validar las opciones Cumplimiento Documentación y Cumplimiento Costo Flete Marítimo')
        msg = 'Favor de aprobar la línea correspondiente al contenedor '  + str(self.container_number)
        self.v_id.activity_schedule(user_id = self.u_aduanal.id, summary =msg , note =msg)
        self.etapa = '2'
        body = " ->Se ha autorizado el pase a la etapa Agente Aduanal por el usuario "+str(self.u_forwarder.name)+' para el contenedor '+str(self.container_number)
        self.v_id.message_post(body=body)
        return self

    def val_aduanal(self):
        """
        1.- Solo el usuario u_aduanal puede ver y autorizar group_agente_auth
        2.-Valida que no hayan menos de 24 horas (o Bloquea el transporte)
        3.-Valida que haya  validado sus campos
        4.-Manda actividades al transportista del la línea
        5.-Pasa de Estapa
        6.-Envía Mensaje al Histórico
        """
        self.val_userid(self.u_aduanal)
        if self.custom_category == '24':
            if self.varevalida  == False or self.vafolio  == False :
                raise ValidationError('Debe Validar las opciones Revalidación del BL y Liberación del Folio')
        if self.custom_category == '36':
            if self.varevalida  == False or self.vaprevio == False:
                raise ValidationError('Debe Validar las opciones Revalidación del BL y Programación del Previo')
        dif =  self.eta_date - datetime.now()
        horas = int(dif.total_seconds()/3600)
        if horas < 24:
            self.etapa = '0'
            body = '->Hay '+str(horas)+' horas de diferencia solo se permiten diferencias mayores a  24 horas entre la la fecha actual y la estimada la línea será Bloqueada'
            self.v_id.message_post(body=body)
            return self
        msg = 'Favor de aprobar la línea correspondente al contenedor '  + str(self.container_number)
        self.v_id.activity_schedule(user_id = self.u_transportista.id, summary =msg , note =msg)
        self.etapa = '3'
        body = " ->Se ha autorizado el pase a la etapa Transportista por el usuario "+str(self.u_aduanal.name)+' para el contenedor '+str(self.container_number)
        self.v_id.message_post(body=body)
        return self

    def val_transportista(self):
        """
        1.- Solo el usuario u_transportista puede ver y autorizar group_trans_auth
        2.-Valida que no hayan menos de 16 horas (o Bloquea el transporte)
        3.-Valida que haya  validado sus campos
        4.-Pasa de Estapa
        5.-Envía Mensaje al Histórico
        """   
        self.val_userid(self.u_transportista)             
        dif =  self.eta_date - datetime.now()
        horas = int(dif.total_seconds()/3600)
        if horas < 16:
            self.etapa = '0'
            body = '->Hay '+str(horas)+' horas de diferencia solo se permiten diferencias mayores a  16 horas entre la la fecha actual y la estimada la línea será Bloqueada'
            self.v_id.message_post(body=body)
            return self
        #validamos que se hallan llenado los campos obligatorios
        if self.vtplaca == False or self.vtconductor == False:
            raise ValidationError('Debe llenar los campos de Placa y Nombre del Conductor') 
        if len(self.vtplaca) < 2   or len(self.vtconductor) < 2:
            raise ValidationError('Debe llenar los campos de Placa y Nombre del Conductor') 
        self.etapa = '4'
        return self

    def val_maniobras(self):
        """
        1.- Solo el usuario u_transportista puede ver y autorizar
        2.-Valida que haya  validado sus campos
        3.-Pasa de Estapa
        4.-Envía Mensaje al Histórico
        """        
        self.val_userid(self.u_transportista)
        if self.vmaniobra == False or self.vflete == False:
            raise ValidationError('Debe Validar la Maniobra de Carga')
        self.etapa = '5'
        body = " ->Se ha autorizado el pase a la etapa Transportista por el usuario "+str(self.u_transportista.name)+' para el contenedor '+str(self.container_number)
        self.v_id.message_post(body=body)
        return self

