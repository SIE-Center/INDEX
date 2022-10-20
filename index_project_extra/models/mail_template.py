from odoo import models, fields, api
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
_logger = logging.getLogger(__name__)

class Index_Mail_Template(models.Model):
    _inherit = 'mail.template'
    reporte = fields.Selection([
    ('1', 'Facturación'),
    ('2', 'Presidencia'),
    ('3', 'Estadísticas Mensuales'),
    ('4', 'General'),
    ('5', 'Incumplimiento'),
], string='Aplicar En')
