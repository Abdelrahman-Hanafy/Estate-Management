from odoo import models, fields


class Owner(models.Model):
    _name = "owner"

    name = fields.Char(string='Name')
    contact_information = fields.Char(string='Phone')
    ownership_percentage = fields.Float(string='Ownership %')

    property_id = fields.Many2one('property', string='Property')

    _sql_constraints = [
        ('phone_number_length_check', "CHECK (contact_information ~ '^\\d{11}$')",
         'Phone number must be 11 characters long.'),
    ]
