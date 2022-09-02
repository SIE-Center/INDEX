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

class Index_Eta_date(models.TransientModel):
    _name = 'index_project_extra.rep_eta_date'
    _description = "Reporte de Proyectos"
    sdate = fields.Datetime('Desde')
    edate = fields.Datetime('Hasta')
    reporte = fields.Selection([
        ('1', 'IMMMEX'),
        ('2', 'Presidencia'),
        ('3', 'Estadística'),
        ('4', 'Facturación'),
    ], string='Reporte')

    def generate(self):
        wb = Workbook() #creamos objeto
        filename = ''
        cand = self.env['custom.vlines'].search([('eta_date','>=',self.sdate),('eta_date','<=',self.edate)])
        if len(cand) == 0:
            raise ValidationError ('No hay contenedores registrados con fecha estimada en el rango provisto')
        if self.reporte == '1':
            wb =self.immex_rep(cand,self.sdate,self.edate,False)
            filename = 'Reporte IMMMEX'
            #Bajamos Excel
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
        return self        

    def immex_rep(self,cand,sdate,edate,immex):
        wb = Workbook() #creamos objeto
        ws = wb.active # inicializamos
        reng = 6 #indicador de renglon
        ws.title = "Solicitud" #titulo
        oper_data = []
        #traemos la imagen configurada en la compañia
        company_id = self.env.company
        if company_id.logo:
            buf_image= BytesIO(base64.b64decode(company_id.logo))
            img = Image(buf_image)
            img.anchor='A1'
            ws.add_image(img)
        ws.cell(4, 4).value = "Global // Immex"
        ws.cell(4, 4).font = Font(size = "15")
        #--------------------Cabecera------------------------------------
        ws['A5'] = 'CATEGORIA'
        ws['B5'] = '#CONTENEDOR'
        ws['C5'] = 'OPERADORA'
        ws['D5'] = 'FECHA DE ETA'
        ws['E5'] = 'FECHA DE DESPACHO'
        for col in range (1,6):
            ws.cell(row=5, column=col).font = Font(color="FFFFFF")
            ws.cell(row=5, column=col).fill = PatternFill('solid', fgColor = '063970')
        for line in cand:
            #si no está en la lista de IMMEX no me importa para el Reporte
            if immex:
                if line.v_id.partner_id not in immex:
                    continue 
            #buscamos la línea origen 
            l_or = self.env['custom.task.line'].search([('task_id','=',line.v_id.id),('container_number','=',line.container_number)],limit = 1)
            cat = ''
            if line.custom_category == '24':
                cat= 'IMMEX 24 hrs'
            if line.custom_category == '36':
                cat= 'IMMEX 36 hrs'
            ws.cell(row=reng, column=1).value = cat #categoría
            ws.cell(row=reng, column=2).value = line.container_number #Contenedor 
            ws.cell(row=reng, column=3).value = str(l_or.operadora.name) #Operadora
            ws.cell(row=reng, column=4).value = line.eta_date #Eta date
            ws.cell(row=reng, column=5).value = str(l_or.dispatch_date)#Fecha de despacho
            #checamos si ya esta en oper_data
            esta = False
            for cd in oper_data:
                if cd[0] == str(l_or.operadora.name):
                    cd[1]= int(cd[1]) + 1
                    esta = True
                    break
            if not esta:
                oper_data.append([str(l_or.operadora.name),1])
            reng = reng + 1
        #--------------Chart Por Operadora---------------------
        #raise ValidationError(str(oper_data))
        ws_chart = wb.create_sheet('Operadora')
        reng = 1
        ws_chart.cell(row=reng, column=1).value = 'Operadora'
        ws_chart.cell(row=reng, column=2).value = 'Contenedores'
        for col in range (1,3):
            ws_chart.cell(row=1, column=col).font = Font(color="FFFFFF")
            ws_chart.cell(row=1, column=col).fill = PatternFill('solid', fgColor = '063970')
        for row in oper_data:
            reng = reng + 1
            ws_chart.cell(row=reng, column=1).value = row[0]
            ws_chart.cell(row=reng, column=2).value = row[1]
        pie = PieChart3D()
        mr = len(oper_data)+1
        labels = Reference(ws_chart, min_col=1, min_row=2, max_row=mr)
        oper_data = Reference(ws_chart, min_col=2, min_row=1, max_row=mr)
        pie.add_data(oper_data, titles_from_data=True)
        pie.set_categories(labels)
        pie.title = "Contenedores por Operadora"
        ws_chart.add_chart(pie, "D2")            
        #-------------Fin de Char por Operadora-------------------------
        return wb



