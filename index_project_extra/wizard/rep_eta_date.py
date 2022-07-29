# -*- coding: utf-8 -*-
import logging
import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from tempfile import NamedTemporaryFile
from datetime import date, timedelta
from odoo.tools.translate import _
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl import Workbook
from openpyxl.writer.excel import ExcelWriter

_logger = logging.getLogger(__name__)

class Index_Eta_date(models.TransientModel):
    _name = 'index_project_extra.rep_eta_date'
    _description = "Reporte de Proyectos"
    sdate = fields.Datetime('Desde')
    edate = fields.Datetime('Hasta')
    bajas = fields.Boolean('Solo Bajas', default = False)

    def generate(self):
        if self.bajas:
            cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate),('etapa','=','0')])
        if self.bajas == False:
            cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate)])
        if len(cand) == 0:
            raise ValidationError ('No hay contenedores registrados con fecha estimada en el rango provisto')
        raise ValidationError ('Encontre '+str(len(cand))+' Contenedeores en ese rango')
        return self