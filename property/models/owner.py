
from odoo import models, fields, api


class Owner(models.Model):
    _name = 'owner'
    name =fields.Char(required=1)
    phone =fields.Char()
    address =fields.Char(required=1)
    property_ids = fields.One2many('property.property','owner_id' , "Properties")