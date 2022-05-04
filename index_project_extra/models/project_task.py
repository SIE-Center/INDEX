# -*- coding: utf-8 -*-
from odoo import models, fields

class Tasks(models.Model):
    _inherit = "project.task"

    custom_category = fields.Selection(
        [('24','24 SIN PREVIO'),('36','36 CON PREVIO')], 
        string="Category"
    )
    bl = fields.Char(string="Bill of Landing (BL)")
    container_number = fields.Char()
    agente_aduanal = fields.Char()
    naviera = fields.Char()
    forwarders = fields.Char()
    operadora = fields.Char()
    buque = fields.Char()
    numero_viaje = fields.Char()
    eta_date = fields.Datetime(string="Fecha ETA")
    previo_date = fields.Datetime(string="Fecha PREVIO")
    dispatch_date = fields.Datetime(string="Fecha Despacho")
    peso = fields.float()
    pieza = fields.Char()

    container_type_id = fields.Many2one('custom.container.type')
    service_type_id = fields.Many2one('custom.service.type')
    packing_type_id = fields.Many2one('custom.packing.type')