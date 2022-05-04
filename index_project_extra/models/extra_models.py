# -*- coding: utf-8 -*-
from odoo import models, fields

class Seasons(models.Model):
    _name = "custom.container.type"

    name = fields.Char()
    code = fields.Char()
    
class Previo(models.Model):
    _name = "custom.service.type"

    name = fields.Char()
    code = fields.Char()
    
class Embalaje(models.Model):
    _name = "custom.packing.type"

    name = fields.Char()
    code = fields.Char()