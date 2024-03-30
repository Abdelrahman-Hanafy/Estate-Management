from odoo import models, fields, api


class PropertyMaintanance(models.Model):
    _name = 'property.maintanance'
    _description = 'Property Maintanance'

    name = fields.Char(string='Name')

    maintenance_type = fields.Selection([
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('inspection', 'Inspection'),
    ], string='Type')

    description = fields.Text(string='Description')

    property_id = fields.Many2one(
        'property', string='Property', default=lambda self: self.env.context.get('property_id', None))
