from odoo import models, fields, api
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
_logger = logging.getLogger(__name__)

class Index_Project_Stage(models.Model):
    _inherit = 'project.task.type'
    emails = fields.Many2many('res.partner', string='Correos para esta etapa')
    attach_name =       fields.Char(string="Nombre de la Imagen")
    attach_document =   fields.Binary(string="Imagen")    

    @api.constrains('attach_name','attach_document')
    def _validate_pic(self):
        if self.attach_name:
            name = str(self.attach_name)
            name = name[-3:].upper()
            if name not in ('PNG','JPG','GIF','BMP'):
                raise ValidationError ('Debe ser un archivo en formato de Imagen')
