from odoo import models, fields


class Transaction(models.Model):
    _name = 'transaction'

    date = fields.Date(string='Date')
    amount = fields.Integer(string='Amount')
    parties_details = fields.Char(string='Parties')

    property = fields.Many2one('property', string='Property')
