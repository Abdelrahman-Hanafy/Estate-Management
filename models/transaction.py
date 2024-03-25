from odoo import models, fields


class Transaction(models.Model):
    """
    This class represents a transaction in the estate management system.
    """
    _name = 'transaction'
    _description = 'Transaction'

    date = fields.Date(string='Date', help='Date of the transaction.')

    amount = fields.Integer(
        string='Amount', help='Amount of the transaction.')

    parties_details = fields.Char(
        string='Parties', help='Parties involved in the transaction.')

    property = fields.Many2one(
        'property', string='Property', help='Property involved in the transaction.')
