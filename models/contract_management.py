from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ContractManagement(models.Model):
    _name = 'estate.contract.management'
    _description = 'Contract Management'

    name = fields.Char(string="Name")
    duration = fields.Integer(string="Duration in Months")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", compute="_compute_end_date")

    offer_id = fields.Many2one('property.offer', string="Offer")

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            rec.end_date = rec.start_date + relativedelta(months=rec.duration)
