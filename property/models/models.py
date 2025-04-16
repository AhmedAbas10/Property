# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests


class property(models.Model):
    _name = 'property.property'
    _description = 'Property Real Estate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    ref = fields.Char()
    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute="_compute_diff", store=True, readonly=0)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default="north")
    owner_id = fields.Many2one('owner', "Owner")
    tags_ids = fields.Many2one('tag', "Tags")
    owner_phone = fields.Char(related='owner_id.phone', readonly=0)
    owner_address = fields.Char(related='owner_id.address', readonly=0)
    line_ids = fields.One2many('property.line', 'property_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default="draft")

    def action_draft(self):
        for rec in self:
            rec.create_property_history(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_property_history(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_property_history(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_property_history(rec.state, 'closed')
            rec.state = 'closed'

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("Please Add Valid Number for Bedrooms !")

    _sql_constraints = [
        ('name_uniq', 'unique("name")', 'Tag name already exists !'),
    ]

    def get_properties(self):
        payload = dict()
        try:
            response = requests.get("localhost:8017//v1/properties", data=payload)
            if response.status_code == 200:
                print("Successful")
            else:
                print("A7A")
        except Exception as Error:
            raise ValidationError(str(Error))

    @api.model
    def create(self, vals):
        res = super(property, self).create(vals)
        if not res.ref:
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('property.property')
        return super(property, self).write(vals)

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                return {
                    'warning': {'title': 'warning', 'message': 'Negative Value', 'type': 'notification'}
                }

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late = True

    def create_property_history(self, old_state, new_state, reason="", dateNow=None):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or " ",
                'dateNow': dateNow,
            })

    def open_change_wizard_action(self):
        action = self.env['ir.actions.actions']._for_xml_id('property.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_related_partner(self):
        action = self.env['ir.actions.actions']._for_xml_id('property.owner_action')
        view_id = self.env.ref('property.owner_form_view').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action


class PropertyLine(models.Model):
    _name = 'property.line'
    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property.property')
