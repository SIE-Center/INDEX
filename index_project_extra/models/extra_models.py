# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date
import logging
from odoo.exceptions import AccessError, UserError, ValidationError

class Seasons(models.Model):
    _name = "custom.container.type"
    _description = "Tipo de Contenedor"
    _rec_name = 'combination'

    name = fields.Char()
    code = fields.Char()
    combination = fields.Char(string='Tipo de Contenedor', compute='_compute_fields_combination')

    @api.depends('name', 'code')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.code  + ' - ' + test.name
    
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         result.append((record.id, record.code))
    #     return result
    
class Previo(models.Model):
    _name = "custom.service.type"
    _description = "Tipo Previo"
    _rec_name = 'combination'

    name = fields.Char()
    code = fields.Char()
    combination = fields.Char(string='Tipo Previo', compute='_compute_fields_combination')

    @api.depends('name', 'code')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.code  + ' - ' + test.name

    
class Embalaje(models.Model):
    _name = "custom.packing.type"
    _description = "Tipo Embalaje"
    _rec_name = 'combination'

    name = fields.Char()
    code = fields.Char()
    combination = fields.Char(string='Tipo Embalaje', compute='_compute_fields_combination')

    @api.depends('name', 'code')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = test.code  + ' - ' + test.name
