from odoo import models, fields


class Owner(models.Model):
    """
    Owners of a property

    Represents the owners of a property in the system, and stores their contact
    information and ownership percentage of the property.
    """

    _name = "owner"
    _description = "Owner"

    name = fields.Char(string='Name')
    contact_information = fields.Char(string='Phone')
    ownership_percentage = fields.Float(string='Ownership %')

    property_id = fields.Many2one('property', string='Property')

    _sql_constraints = [
        ('phone_number_length_check', "CHECK (contact_information ~ '^\\d{11}$')",
         'Phone number must be 11 characters long.'),
    ]
