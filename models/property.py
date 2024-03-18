from odoo import models, fields, api


class Property(models.Model):
    _name = "property"

    # The name or identifier of the property (e.g., “Luxury Villa,” “Apartment 3B”).
    name = fields.Char(string='Name')
    # The physical address of the property.
    address = fields.Char(string='Address')
    # The type of property (e.g., residential, commercial, land).
    property_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('land', 'Land')
    ], string='Type')
    # The size of the property (in square meters or square feet).
    # computed field for square meters
    size = fields.Float(compute="_compute_size", string='Size')
    width = fields.Float(string='Width')
    height = fields.Float(string='Height')
    # The selling or rental price of the property.
    price = fields.Integer(string='Price')
    # Additional details about the property.
    description = fields.Text(string='Description')

    owners = fields.One2many('owner', 'property_id', string="Owners")
    tenant = fields.Many2one('tenant', string='Tenants')

    @api.depends("width", "height")
    def _compute_size(self):
        for record in self:
            record.size = record.width * record.height
