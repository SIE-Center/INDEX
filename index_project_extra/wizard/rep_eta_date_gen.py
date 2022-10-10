# -*- coding: utf-8 -*-
import logging
import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from tempfile import NamedTemporaryFile
from datetime import date, timedelta
from odoo.tools.translate import _
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl import Workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.chart import   Reference,BarChart
from openpyxl.chart.label import DataLabelList
from io import BytesIO 
import base64
_logger = logging.getLogger(__name__)

class Index_Eta_Date_Gen(models.TransientModel):
    _name = 'index_project_extra.rep_eta_date_gen'
    _description = "Reporte de Tareas"
    sdate = fields.Datetime('Desde')
    edate = fields.Datetime('Hasta')

    def generate_gen(self):
        user = self.env['res.users'].browse(self._context.get('uid'))
        if not user.partner_id:
            raise ValidationError('El Usuario no tiene un IMMEX Relacionado')
        if user.partner_id.category_id.name !='IMMEX':
            raise ValidationError('El Proveedor Relacionado a este Usuario no esta Marcado como IMMEX')
        #Si llegamos hasta aqui entonces se trata de un Immex Válido
        #-------------Traemos los Datos Para el Reporte General
        cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate),('etapa','in',('0','5','6'))]) 
        if len(cand) == 0:
            raise ValidationError ('No hay contenedores registrados con fecha estimada en el rango provisto')
        wb =self.env['index_project_extra.rep_eta_date'].general(cand,self.sdate,self.edate,user.partner_id)
        filename = 'Reporte General '+user.partner_id.name+'.xlsx'
        with NamedTemporaryFile() as tmp: #graba archivo temporal
            wb.save(tmp.name) #graba el contenido del excel en tmp.name
            output = tmp.read()
        xlsx = {                            #características del archivo
                'name': filename,
                'type': 'binary',
                'res_model': 'selmrp.tmpexploit',
                'datas': base64.b64encode(output),  #aqui metemos el archivo generado y grabado
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                }
        inserted_id=self.env['ir.attachment'].create(xlsx) # creamos el link de download
        url='/web/content/%s?download=1' %(inserted_id.id)
        return {'type': 'ir.actions.act_url','name': filename,'url': url} #regresamos el link con el archivo         
