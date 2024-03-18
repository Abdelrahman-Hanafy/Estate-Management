from datetime import timedelta
from odoo import models, fields, api


class PropertyOffer(models.Model):
    _name = 'property.offer'
    _sql_constraints = [
        ('price_positive_check', "CHECK (price >= 0)", 'Price must be positive.'),
    ]
    # name = fields.Char(string='Name', required=True)
    # description = fields.Text(string='Description')

    price = fields.Float(string='Price', required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='pending', string='State')

    validity = fields.Integer(string='Validity (days)', default=7)

    #  A computed field defined as the sum of two fields: create_date, validity
    date_deadline = fields.Date(
        string='Deadline', compute="_compute_date_deadline",
        inverse="_set_date_deadline", store=True
    )

    property_id = fields.Many2one('property', string='Property', required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + \
                timedelta(days=record.validity)

    def _set_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days
