# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
from datetime import datetime, date
from odoo.exceptions import AccessError, UserError, ValidationError
_logger = logging.getLogger(__name__)

class RepConf(models.Model):
    _name = "custom.repconf"
    _description = "Configuración de Envio de reportes"
    _rec_name = 'name'
    name =   fields.Char('Nombre')
    sdate = fields.Datetime('Desde')
    edate = fields.Datetime('Hasta')
    index =  fields.Many2many('res.partner', string='Index')
    emails_l = fields.Text(string="Emails List")
    rep_1 =  fields.Boolean('IMMMEX')
    rep_2 =  fields.Boolean('Presidencia')
    rep_3 =  fields.Boolean('Estadística')
    rep_4 =  fields.Boolean('Facturación')
    