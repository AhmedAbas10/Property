from odoo import fields, models, api


class PropertyHistory(models.Model):
    _name = 'property.history'
    _rec_name = "property_id"
    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property.property')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()
    dateNow = fields.Date(default=fields.date.today())
