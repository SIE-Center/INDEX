from odoo import models, fields, api
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
_logger = logging.getLogger(__name__)

class Index_Project_Stage(models.Model):
    _inherit = 'project.task.type'
    emails = fields.Many2many('res.partner', string='Correos para esta etapa')