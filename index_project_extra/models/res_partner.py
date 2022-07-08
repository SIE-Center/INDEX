from odoo import models, fields, api
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
_logger = logging.getLogger(__name__)

class Index_Res_Partner(models.Model):
    _inherit = 'res.partner'
    partners_ids = fields.One2many('index_project_extra.partner_lines', 'index_partner_id',string ="Proveedores")
    email2 =  fields.Char('Correo electrónico 2')
    

class Index_Res_Partner_Lines(models.Model):
    _name = "index_project_extra.partner_lines"
    index_partner_id =  fields.Many2one('res.partner')
    partner =           fields.Many2many('res.partner', string='Proveedor')
    partner_type =      fields.Selection([('F', 'Forwarder'),('A', 'Agente Aduanal'),('T', 'Transportista'),('O', 'Operadora')], string='Tipo de Proveedor')
    
