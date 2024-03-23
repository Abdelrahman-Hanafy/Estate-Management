from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ContractManagement(models.Model):
    _name = 'estate.contract.management'
    _description = 'Contract Management'

    name = fields.Char(
        string="Name", default=lambda self: self.env.context.get('name', ''))
    duration = fields.Integer(string="Duration in Months", default=1)
    start_date = fields.Date(string="Start Date", default=fields.Date.today())
    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    offer_id = fields.Many2one('property.offer', string="Offer",
                               default=lambda self: self.env.context.get('offer_id', None))

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            rec.end_date = rec.start_date + \
                relativedelta(months=rec.duration)
