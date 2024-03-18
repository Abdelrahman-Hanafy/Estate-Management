from odoo import models, fields, api
from datetime import datetime, timedelta


class Property(models.Model):
    _name = "property"
    _sql_constraints = [
        ('price_positive_check', "CHECK (price >= 0)", 'Price must be positive.'),
    ]

    # The name or identifier of the property (e.g., “Luxury Villa,” “Apartment 3B”).
    name = fields.Char(string='Name', required=True)
    # The physical address of the property.
    address = fields.Char(string='Address')
    # The type of property (e.g., residential, commercial, land).
    property_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('land', 'Land')
    ], string='Type', required=True)

    # The size of the property (in square meters or square feet).
    # computed field for square meters
    size = fields.Float(compute="_compute_size", string='Size')
    width = fields.Float(string='Width')
    height = fields.Float(string='Height')

    # The selling or rental price of the property.
    price = fields.Integer(string='Price', required=True)
    # Additional details about the property.
    description = fields.Text(string='Description')

    # Represents the current state of the property (e.g., available, rented, under maintenance)
    state = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('under_maintenance', 'Under Maintenance')
    ], default='available', string='State')

    bedrooms = fields.Integer(string='Bedrooms', default=2)

    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')

    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)', default=10)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north')

    availability_date = fields.Datetime(
        string='Availability Date', default=lambda _: datetime.now() + timedelta(days=90))

    owners = fields.One2many('owner', 'property_id', string="Owners")
    tenant = fields.Many2one('tenant', string='Tenants')

    @api.depends("width", "height")
    def _compute_size(self):
        for record in self:
            record.size = record.width * record.height

    def mark_Available(self):
        for record in self:
            record.state = "available"
        return True

    def mark_Rented(self):
        for record in self:
            record.state = "rented"
        return True

    def mark_Under_Maintenance(self):
        for record in self:
            record.state = "under_maintenance"
        return True
