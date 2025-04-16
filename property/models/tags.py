
from odoo import models, fields, api


class Owner(models.Model):
    _name = 'tag'
    name =fields.Char(required=1)
