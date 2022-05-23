# -*- coding: utf-8 -*-
from odoo import models, fields

class Tasks(models.Model):
    _inherit = "project.task"

    custom_task_line_ids = fields.One2many(comodel_name='custom.task.line', inverse_name='task_id')