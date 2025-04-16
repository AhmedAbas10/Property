from odoo import models, fields


class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property.property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], default="draft")
    reason = fields.Char()
    dateNow = fields.Date(default=fields.date.today())


    def action_confirm(self):
        if self.property_id.state == 'closed':
            self.property_id.state = self.state
            self.property_id.create_property_history('closed', self.state, self.reason, self.dateNow)
