from odoo import models, fields


class Tenant(models.Model):
    _name = 'tenant'

    name = fields.Char(string='Name')
    contact_information = fields.Char(string='Phone')
    lease_start_date = fields.Date(string='St_date')
    lease_end_date = fields.Date(string='End_date')
    monthly_rent = fields.Integer(string='Rent')

    _sql_constraints = [
        ('phone_number_length_check', "CHECK (contact_information ~ '^\\d{11}$')",
         'Phone number must be 11 characters long.'),
    ]
