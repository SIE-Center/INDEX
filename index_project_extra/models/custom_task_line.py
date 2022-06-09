# -*- coding: utf-8 -*-
from email.policy import default
from odoo import models, fields

class TaskLines(models.Model):
    _name = "custom.task.line"

    task_id = fields.Many2one('project.task')
    custom_category = fields.Selection(
        [('24','24 SIN PREVIO'),('36','36 CON PREVIO')], 
        string="Categoría",
        default='24'
    )
    bl = fields.Char(string="Bill of Landing (BL)")
    container_number = fields.Char(string="Número Contenedor")
    agente_aduanal = fields.Char()
    naviera = fields.Char()
    forwarders = fields.Char()
    operadora = fields.Char()
    buque = fields.Char()
    numero_viaje = fields.Char()
    eta_date = fields.Datetime(string="Fecha ETA")
    previo_date = fields.Datetime(string="Fecha PREVIO")
    dispatch_date = fields.Datetime(string="Fecha Despacho")
    peso = fields.Float()
    pieza = fields.Char()

    container_type_id = fields.Many2one('custom.container.type', string="Tipo Contenedor")
    service_type_id = fields.Many2one('custom.service.type', string="Tipo Previo")
    packing_type_id = fields.Many2one('custom.packing.type', string="Tipo Embalaje")