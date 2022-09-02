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
from openpyxl.chart import  PieChart3D, Reference
from io import BytesIO 
import base64
_logger = logging.getLogger(__name__)

class RepConf(models.Model):
    _name = "custom.repconf"
    _description = "Configuración de Envio de reportes"
    _rec_name = 'name'
    name =   fields.Char('Nombre')
    sdate = fields.Datetime('Desde')
    edate = fields.Datetime('Hasta')
    index =  fields.Many2many('res.partner', string='Immex')
    emails_l = fields.Text(string="Emails List")
    rep_1 =  fields.Boolean('IMMMEX')
    rep_2 =  fields.Boolean('Presidencia')
    rep_3 =  fields.Boolean('Estadística')
    rep_4 =  fields.Boolean('Facturación')
    
    def send_mails(self):
        wb = Workbook() #creamos objeto
        filename = ''
        cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate)])
        if cand == False:
            raise ValidationError('No hay Registros en ese Rango de Fechas')
        cuantos = 0
        for c in cand:
            if c.v_id.partner_id in self.index:
                cuantos = cuantos + 1
        if cuantos == 0:
            raise ValidationError('No hay Registros en ese Rango de Fechas para los IMMEX Seleccionados')
        #---------------------------------->Reporte Immex<-----------------------------------------------------
        if self.rep_1:
            wb = self.env['index_project_extra.rep_eta_date'].immex_rep(cand,self.sdate,self.edate,self.index)
            filename = 'Reporte IMMMEX'
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
            body_mail = 'Buen día' +'\n'+' Envio de Reporte Immex.'
            body_mail_html = '<p>Buen d&iacute;a.</p><p> Reporte IMMEX</p>'
            mail_pool = self.env['mail.mail']
            values={}
            values.update({'subject': 'Reporte Immex'})
            values.update({'email_to': self.emails_l})
            values.update({'body_html': body_mail_html })
            values.update({'body': body_mail })
            values.update({'attachment_ids': inserted_id })
            values.update({'res_id': self.id }) #[optional] here is the record id, where you want to post that email after sending
            values.update({'model': 'custom.repconf' }) #[optional] here is the object(like 'project.project')  to whose record id you want to post that email after sending
            msg_id = mail_pool.sudo().create(values)
            if msg_id:
                mail_pool.send([msg_id])            
        #---------------------------------->Reporte Immex<-----------------------------------------------------
        return self