# -*- coding: utf-8 -*-
import string
from odoo import models, fields

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
    buque = fields.Char()
    numero_viaje = fields.Char()
    eta_date = fields.Datetime(string="Fecha ETA")
    previo_date = fields.Datetime(string="Fecha PREVIO")
    dispatch_date = fields.Datetime(string="Fecha Despacho")
    peso = fields.Float()
    pieza = fields.Char()
    container_type_id = fields.Many2one('custom.container.type',string = "Tipo de Contenedor")
    service_type_id = fields.Many2one('custom.service.type',string = "Tipo Previo")
    packing_type_id = fields.Many2one('custom.packing.type',string = "Tipo Embalaje")