# -*- coding: utf-8 -*-
import logging
import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from tempfile import NamedTemporaryFile
from datetime import datetime
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
    rep_1 =  fields.Boolean('Facturación')
    rep_2 =  fields.Boolean('Presidencia')
    rep_3 =  fields.Boolean('Estadísticas Mensuales')
    rep_4 =  fields.Boolean('General')
    rep_5 =  fields.Boolean('Incumplimiento')
    u_env =  fields.Datetime('Último Envío')

    @api.onchange('index')
    def _fill_index(self):
        l = []
        indx = self.env['res.partner'].search([('category_id','!=',False)])
        if indx:
            for i in indx:
                for n in i.category_id:
                    if n.name == 'IMMEX':
                        l.append(int(i.id))
        return {'domain': {'index': [('id', 'in', l)]}}     
    
    def send_mails(self):
        wb = Workbook() #creamos objeto
        filename = ''
        cand = False
        if self.rep_1:#IMMEX
            cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate)])
        if self.rep_2:#Presidencia
            cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate),('etapa','in',('0','5','6'))])
        if self.rep_3:#Estadísticas Mensuales
            cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate),('etapa','in',('5','6'))])
        if self.rep_4:#General
            cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate),('etapa','in',('0','5','6'))])
        if self.rep_5:#Incumplimiento
            cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate),('etapa','in',('0','6'))])
        if cand == False:
            raise ValidationError('No hay Registros en ese Rango de Fechas')
        cuantos = 0
        for c in cand:
            if c.v_id.partner_id in self.index:
                cuantos = cuantos + 1
        #if cuantos == 0:
        #    raise ValidationError('No hay Registros en ese Rango de Fechas para los IMMEX Seleccionados')
        #---------------------------------->Reporte Immex<-----------------------------------------------------
        if self.rep_1:
            wb = self.env['index_project_extra.rep_eta_date'].immex_rep(cand,self.sdate,self.edate,self.index)
            filename = 'Reporte Facturación IMMMEX.xlsx'
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
            mail_pool = self.env['mail.template'].search([('reporte','=','1')])
            if not mail_pool:
                raise ValidationError('No hay una Plantilla de correo para el Reporte Facturación IMMMEX')
            mail_pool.email_to = str(self.emails_l)
            mail_pool.attachment_ids = [(6,0, [inserted_id.id])]
            mail_pool.send_mail(res_id=self.id , force_send = True, raise_exception=False, email_values=None, notif_layout=False)
            mail_pool.attachment_ids = [(3,inserted_id.id)]
            mail_pool.email_to = False
        #---------------------------------->Reporte Immex<-----------------------------------------------------
        #---------------------------------->Reporte Presidencia<-----------------------------------------------------
        if self.rep_2:
            wb = self.env['index_project_extra.rep_eta_date'].presidencia(cand,self.sdate,self.edate,self.index)
            filename = 'Reporte Presidencia.xlsx'
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
            mail_pool = self.env['mail.template'].search([('reporte','=','2')])
            if not mail_pool:
                raise ValidationError('No hay una Plantilla de correo para el Reporte de Presidencia')
            mail_pool.email_to = str(self.emails_l)
            mail_pool.attachment_ids = [(6,0, [inserted_id.id])]
            mail_pool.send_mail(res_id=self.id , force_send = True, raise_exception=False, email_values=None, notif_layout=False)
            mail_pool.attachment_ids = [(3,inserted_id.id)]
            mail_pool.email_to = False
        #---------------------------------->Reporte Presidencia<-----------------------------------------------------
        #---------------------------------->Reporte Estadística<-----------------------------------------------------
        if self.rep_3:
            wb = self.env['index_project_extra.rep_eta_date'].estadistica(cand,self.sdate,self.edate,self.index)
            filename = 'Reporte Estadística.xlsx'
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
            mail_pool = self.env['mail.template'].search([('reporte','=','3')])
            if not mail_pool:
                raise ValidationError('No hay una Plantilla de correo para el Reporte de  Estadísticas  Mensuales')
            mail_pool.email_to = str(self.emails_l)
            mail_pool.attachment_ids = [(6,0, [inserted_id.id])]
            mail_pool.send_mail(res_id=self.id , force_send = True, raise_exception=False, email_values=None, notif_layout=False)
            mail_pool.attachment_ids = [(3,inserted_id.id)]
            mail_pool.email_to = False
        #---------------------------------->Reporte Estadística<-----------------------------------------------------
        #---------------------------------->Reporte General<-----------------------------------------------------
        if self.rep_4:
            wb = self.env['index_project_extra.rep_eta_date'].general(cand,self.sdate,self.edate,self.index)
            filename = 'Reporte General.xlsx'
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
            mail_pool = self.env['mail.template'].search([('reporte','=','4')])
            if not mail_pool:
                raise ValidationError('No hay una Plantilla de correo para el Reporte General')
            mail_pool.email_to = str(self.emails_l)
            mail_pool.attachment_ids = [(6,0, [inserted_id.id])]
            mail_pool.send_mail(res_id=self.id , force_send = True, raise_exception=False, email_values=None, notif_layout=False)
            mail_pool.attachment_ids = [(3,inserted_id.id)]
            mail_pool.email_to = False
        #---------------------------------->Reporte Incumplimiento<-----------------------------------------------------
        if self.rep_5:
            wb = self.env['index_project_extra.rep_eta_date'].general(cand,self.sdate,self.edate,self.index)
            filename = 'Reporte Incumplimiento.xlsx'
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
            mail_pool = self.env['mail.template'].search([('reporte','=','5')])
            if not mail_pool:
                raise ValidationError('No hay una Plantilla de correo para el Reporte de Incumplimiento')
            mail_pool.email_to = str(self.emails_l)
            mail_pool.attachment_ids = [(6,0, [inserted_id.id])]
            mail_pool.send_mail(res_id=self.id , force_send = True, raise_exception=False, email_values=None, notif_layout=False)
            mail_pool.attachment_ids = [(3,inserted_id.id)]
            mail_pool.email_to = False
        #---------------------------------->Reporte General<-----------------------------------------------------
        #self.u_env = datetime.strftime(fields.Datetime.context_timestamp(self, datetime.now()), "%Y-%m-%d %H:%M:%S")
        _logger.error("------------------------------------>"+str(self.emails_l))
        self.u_env = datetime.now()
        return self