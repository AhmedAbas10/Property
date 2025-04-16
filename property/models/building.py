# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Building(models.Model):
    _name = 'building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = "code"
    name=fields.Char()
    no =fields.Integer()
    description = fields.Text(tracking=1)
    code = fields.Char()
    active = fields.Boolean(default=True)