from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class LeaseAgreement(models.Model):
    _name = 'lease.agreement'
    _description = 'Lease Agreement'

    name = fields.Char(string='Name')
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    end_date = fields.Date(string='End Date', compute='_compute_end_date')
    duration = fields.Integer(string='Duration', default=1)

    # relation fields
    offer_id = fields.Many2one('property.offer', string="Offer",
                               help="Offer related to the agreement")
    price = fields.Float(string="Price", related='offer_id.price')

    property_id = fields.Many2one(
        'property', string='Property', related='offer_id.property_id')

    tenant_id = fields.Many2one(
        'tenant', string='Tenant', related='offer_id.tenant_id'
    )

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):

        for rec in self:
            rec.end_date = rec.start_date + \
                relativedelta(months=rec.duration)
