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
    etapa =fields.Selection([('0','Bloqueada'),('1','Forwarder'),('2','Agente Aduanal'),('3','Transportista'),('4','Maniobras de Carga'),('5','Finalizada')], 
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

    def val_forwarder(self):
        if self.vfdocs == False or self.vflete == False:
            raise ValidationError('Debe Validar las opciones Cumplimiento Documentación y Cumplimiento Costo Flete Marítimo')
        self.etapa = '2'
        return self

    def val_aduanal(self):
        if self.custom_category == '24':
            if self.varevalida  == False or self.vafolio  == False :
                raise ValidationError('Debe Validar las opciones Revalidación del BL y Liberación del Folio')
        if self.custom_category == '36':
            if self.varevalida  == False or self.vaprevio == False:
                raise ValidationError('Debe Validar las opciones Revalidación del BL y Programación del Previo')
        self.etapa = '3'
        return self

    def val_transportista(self):
        #validamos que se hallan llenado los campos obligatorios
        if self.vtplaca == False or self.vtconductor == False:
            raise ValidationError('Debe llenar los campos de Placa y Nombre del Conductor') 
        if len(self.vtplaca) < 2   or len(self.vtconductor) < 2:
            raise ValidationError('Debe llenar los campos de Placa y Nombre del Conductor') 
        self.etapa = '4'
        return self

    def val_maniobras(self):
        if self.vmaniobra == False or self.vflete == False:
            raise ValidationError('Debe Validar la Maniobra de Carga')
        self.etapa = '5'
        return self

