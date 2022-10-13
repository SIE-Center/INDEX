# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date
import logging
from odoo.exceptions import AccessError, UserError, ValidationError

class Seasons(models.Model):
    _name = "custom.container.type"
    _description = "Tipo de Contenedor"
    _rec_name = 'name'

    name = fields.Char()
    code = fields.Char()
    combination = fields.Char(string='Tipo de Contenedor', compute='_compute_fields_combination')

    @api.depends('name', 'code')
    def _compute_fields_combination(self):
        for test in self:
            if  test.code and test.name:
                test.combination = str(test.code)  + ' - ' + str(test.name)
            else: 
                test.combination = ' '

    
    
class Previo(models.Model):
    _name = "custom.service.type"
    _description = "Tipo Previo"
    _rec_name = 'name'

    name = fields.Char()
    code = fields.Char()
    combination = fields.Char(string='Tipo Previo', compute='_compute_fields_combination')

    @api.depends('name', 'code')
    def _compute_fields_combination(self):
        for test in self:
            if  test.code and test.name:
                test.combination = str(test.code)  + ' - ' + str(test.name)
            else: 
                test.combination = ' '


    
class Embalaje(models.Model):
    _name = "custom.packing.type"
    _description = "Tipo Embalaje"
    _rec_name = 'name'

    name = fields.Char()
    code = fields.Char()
    combination = fields.Char(string='Tipo Embalaje', compute='_compute_fields_combination')

    @api.depends('name', 'code')
    def _compute_fields_combination(self):
        for test in self:
            if  test.code and test.name:
                test.combination = str(test.code)  + ' - ' + str(test.name)
            else: 
                test.combination = ' '

