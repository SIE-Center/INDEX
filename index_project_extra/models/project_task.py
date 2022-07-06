# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from tempfile import NamedTemporaryFile
from datetime import datetime, date
from odoo.tools.translate import _
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl import Workbook
import base64
_logger = logging.getLogger(__name__)

class Tasks(models.Model):
    _inherit = "project.task"

    custom_task_line_ids = fields.One2many(comodel_name='custom.task.line', inverse_name='task_id')

    def send_email(self):
        #Iniciamos con la cabecera del Excel
        wb = Workbook() #creamos objeto
        ws = wb.active # inicializamos
        reng = 5 #indicador de renglon
        ws.title = "Solicitud" #titulo
        ws.cell(2, 2).value = "Solicitud de Marca de Calidad IMMEX"
        ws.cell(2, 2).font = Font(size = "15")
        #--------------------Cabecera------------------------------------
        ws['A4'] = 'CATEGORIA'
        ws['B4'] = 'BL'
        ws['C4'] = '#CONTENEDOR'
        ws['D4'] = 'TIPO DE CONTENEDOR'
        ws['E4'] = 'ID AGENTE ADUANAL'
        ws['F4'] = 'ID NAVIERA'
        ws['G4'] = 'ID FORWARDERS'
        ws['H4'] = 'OPERADORA'
        ws['I4'] = 'BUQUE'
        ws['J4'] = 'NO. VIAJE'
        ws['K4'] = 'FECHA DE ETA'
        ws['L4'] = 'FECHA PREVIO'
        ws['M4'] = 'PREVIO'
        ws['N4'] = 'PESO'
        ws['O4'] = 'PIEZAS'
        ws['P4'] = 'EMBALAJE'
        ws['Q4'] = 'FECHA SALIDA'
        ws['R4'] = 'TIPO DE SERVICIO'
        for col in range (1,19):
            ws.cell(row=4, column=col).font = Font(color="FFFFFF")
            ws.cell(row=4, column=col).fill = PatternFill('solid', fgColor = '063970')

        #Traemos todos los clientes activos 
        for i in self.custom_task_line_ids:
            ws.cell(row=reng, column=1).value = i.custom_category
            ws.cell(row=reng, column=2).value = i.bl
            ws.cell(row=reng, column=3).value = i.container_number
            ws.cell(row=reng, column=4).value = str(i.container_type_id.name)
            ws.cell(row=reng, column=5).value = i.agente_aduanal.name
            ws.cell(row=reng, column=6).value = i.naviera
            ws.cell(row=reng, column=7).value = i.forwarders.name
            ws.cell(row=reng, column=8).value = i.operadora.name
            ws.cell(row=reng, column=9).value = i.buque
            ws.cell(row=reng, column=10).value = i.numero_viaje
            ws.cell(row=reng, column=11).value = i.eta_date
            ws.cell(row=reng, column=12).value = i.previo_date
            ws.cell(row=reng, column=13).value = i.peso
            ws.cell(row=reng, column=14).value = i.pieza
            ws.cell(row=reng, column=15).value = str(i.packing_type_id.name)
            ws.cell(row=reng, column=17).value = str(i.dispatch_date)
            ws.cell(row=reng, column=18).value = str(i.service_type_id.name)
            reng = reng + 1
        with NamedTemporaryFile() as tmp: #graba archivo temporal
            wb.save(tmp.name) #graba el contenido del excel en tmp.name
            output = tmp.read()
        filename = 'Solicitud De Marca%s.xlsx' % (date.today().strftime('%Y%m%d')) #nombre del archivo en Excel
        xlsx = {                            #características del archivo
                'name': filename,
                'type': 'binary',
                'res_model': 'selmrp.tmpexploit',
                'datas': base64.b64encode(output),  #aqui metemos el archivo generado y grabado
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                }
        inserted_id=self.env['ir.attachment'].create(xlsx) # creamos el link de download
        url='/web/content/%s?download=1' %(inserted_id.id)
        #obtenemos la lista de todos los emails a mandar
        #primero vamos por los que tiene el reporte 
        l_mails = []
        for i in self.custom_task_line_ids:
            if i.forwarders.email == False:
                raise ValidationError('El Forwarder '+str(i.forwarders.name)+' No tiene correo Asignado se cancela la operación')
            if i.operadora.email == False:
                raise ValidationError('La Operadora  '+str(i.operadora.name)+' No tiene correo Asignado se cancela la operación')
            if i.agente_aduanal.email == False:
                raise ValidationError('El Agente Aduanal'+str(i.agente_aduanal.name)+' No tiene correo Asignado se cancela la operación')
            l_mails.append(i.forwarders.email)
            l_mails.append(i.operadora.email)
            l_mails.append(i.agente_aduanal.email)
                
        #ahora vamos por la lista de correos de la etapa

        for lm in self.stage_id.emails:
                if lm.email:
                    l_mails.append(lm.email)
        #seguramente hay duplicados vamos a eliminarlos
        l_mails = list(dict.fromkeys(l_mails))
        emto = ''
        for lm in l_mails:
            emto = emto + lm + ','
        #ya tenemos todo mandemos el correo
        mail_pool = self.env['mail.mail']
        values={}
        values.update({'subject': self.name})
        values.update({'email_to': emto})
        values.update({'body_html': self.name })
        values.update({'body': self.name })
        values.update({'attachment_ids': inserted_id })
        values.update({'res_id': self.id }) #[optional] here is the record id, where you want to post that email after sending
        values.update({'model': 'project.task' }) #[optional] here is the object(like 'project.project')  to whose record id you want to post that email after sending
        msg_id = mail_pool.create(values)
        if msg_id:
            mail_pool.send([msg_id])
        return {'type': 'ir.actions.act_url','name': filename,'url': url} #regresamos el link con el archivo         


        
        