# -*- coding: utf-8 -*-
import string
from odoo import models, fields, api
import logging
from datetime import datetime, date
from odoo.exceptions import AccessError, UserError, ValidationError
_logger = logging.getLogger(__name__)

class TaskLines(models.Model):
    _name = "custom.task.line"

    task_id = fields.Many2one('project.task')
    custom_category = fields.Selection(
        [('24','IMMEX 24 hrs'),('36','IMMEX 36 hrs')], 
        string="Categoría"
    )
    bl = fields.Char(string="Bill of Landing (BL)")
    container_number = fields.Char("Nro. Container")
    agente_aduanal = fields.Many2one('res.partner', string='Agente Aduanal')
    naviera = fields.Char()
    forwarders =  fields.Many2one('res.partner', string='Forwarder')
    operadora =   fields.Many2one('res.partner', string='Operadora')
    transportista =   fields.Many2one('res.partner', string='Transportista')
    buque = fields.Char()
    numero_viaje = fields.Char()
    eta_date = fields.Datetime(string="Fecha ETA")
    previo_date = fields.Datetime(string="Fecha PREVIO")
    dispatch_date = fields.Datetime(string="Fecha Despacho")
    peso = fields.Float()
    pieza = fields.Char()
    container_type_id = fields.Many2one('custom.container.type',string = "Tipo de Contenedor")
    service_type_id = fields.Many2one('custom.service.type',string = "Tipo Previo")
    #packing_type_id = fields.Many2one('custom.packing.type',string = "Tipo Embalaje")
    packing_type_id = fields.Many2many('custom.packing.type', string='Tipo Embalaje')


    @api.onchange('eta_date')
    def _validate_eta(self):
        if self.eta_date != False:
            dif =  self.eta_date - datetime.now()
            horas = int(dif.total_seconds()/3600)
            if horas < 48:
                raise ValidationError('Hay '+str(horas)+' horas de diferencia solo se permiten diferencias mayores a 48 horas entre la la fecha actual y la estimada' )

        
    @api.onchange('transportista')
    def _fill_transportista(self):
        l = []
        for i in self.task_id.partner_id.partners_ids:
            if i.partner_type == 'T':
                for j in i.partner:
                    l.append(int(j.id))
        return {'domain': {'transportista': [('id', 'in', l)]}}     

    @api.onchange('agente_aduanal')
    def _fill_agente_aduanal(self):
        l = []
        for i in self.task_id.partner_id.partners_ids:
            if i.partner_type == 'A':
                for j in i.partner:
                    l.append(int(j.id))
        return {'domain': {'agente_aduanal': [('id', 'in', l)]}}     

    @api.onchange('forwarders')
    def _fill_forwarders(self):
        l = []
        for i in self.task_id.partner_id.partners_ids:
            if i.partner_type == 'F':
                for j in i.partner:
                    l.append(int(j.id))
        return {'domain': {'forwarders': [('id', 'in', l)]}}     

    @api.onchange('operadora')
    def _fill_operadora(self):
        l = []
        for i in self.task_id.partner_id.partners_ids:
            if i.partner_type == 'O':
                for j in i.partner:
                    l.append(int(j.id))
        return {'domain': {'operadora': [('id', 'in', l)]}}            

