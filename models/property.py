from odoo import models, fields, api
from datetime import timedelta


class Property(models.Model):
    """
    A property can be a residential, commercial or land property. 
    It has a name, a property type, an address, a size, a price and a description.
    It can also have additional features like bedrooms, living area, facades, garage, garden, etc.
    The state of the property is one of available, rented or under maintenance.
    """
    _name = "property"
    _description = "Property"

    _sql_constraints = [
        ('price_positive_check', "CHECK (price >= 0)", 'Price must be positive.'),
    ]

    # The name or identifier of the property (e.g., “Luxury Villa,” “Apartment 3B”).
    name = fields.Char(string='Name', required=True,
                       help="The name of the property")
    # The physical address of the property.
    address = fields.Char(string='Address', help="The address of the property")
    # The type of property (e.g., residential, commercial, land).
    property_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('land', 'Land')
    ], string='Type', required=True, help="The type of the property")

    # The size of the property (in square meters or square feet).
    # computed field for square meters
    size = fields.Float(compute="_compute_size", string='Size',
                        help="The size of the property in square meters")
    width = fields.Float(string='Width', help="The width of the property")
    height = fields.Float(string='Height', help="The height of the property")

    # The selling or rental price of the property.
    price = fields.Integer(string='Price', required=True,
                           help="The selling or rental price of the property")
    # Additional details about the property.
    description = fields.Text(string='Description',
                              help="Additional details about the property")

    # Represents the current state of the property (e.g., available, rented, under maintenance)
    state = fields.Selection([
        ('new', 'New'),
        ('available', 'Available'),
        ('offer_received', 'Offer Received'),
        ('rented', 'Rented'),
        ('under_maintenance', 'Under Maintenance')
    ], default='new', string='State',
        help="The current state of the property")

    # The availability date of the property
    availability_date = fields.Datetime(string='Availability Date',
                                        default=lambda self: self._compute_default_availability_date(),
                                        help="The date from when the property is available")

    # The best offer for the property based on its offers
    best_offer = fields.Float(string='Best Offer', compute="_compute_best_offer", store=True,
                              help="The best offer for this property")

    # Additional features of the property
    ########################################################################

    # The number of bedrooms of the property
    bedrooms = fields.Integer(
        string='Bedrooms', default=2, help="The number of bedrooms of the property")
    # The living area of the property
    living_area = fields.Integer(string='Living Area (sqm)',
                                 help="The living area of the property in square meters")
    # The number of facades of the property
    facades = fields.Integer(
        string='Facades', help="The number of facades of the property")
    # Whether the property has a garage or not
    garage = fields.Boolean(
        string='Garage', help="Whether the property has a garage or not")

    # The garden features of the property
    garden = fields.Boolean(
        string='Garden', help="Whether the property has a garden or not")
    garden_area = fields.Integer(string='Garden Area (sqm)', default=0,
                                 help="The garden area of the property in square meters")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation',
        help="The orientation of the garden of the property")

    ########################################################################

    # Start of relational fields
    ########################################################################

    # The owners of the property
    owner_ids = fields.One2many('owner', 'property_id',
                                string="Owners", help="The owners of the property")

    # The tenant who currently occupies the property
    tenant_id = fields.Many2one(
        'tenant',
        string='Tenants',
        help="The tenant who currently occupies the property"
    )

    # The offers for the property
    offer_ids = fields.One2many(
        'property.offer',
        'property_id',
        string="Offers",
        help="The list of offers for this property"
    )

    documents_ids = fields.One2many(
        'property.document',
        'property_id',
        string="Documents",
        help="The list of documents for this property"
    )

    ########################################################################

    def _compute_default_availability_date(self):
        """
        Set the default value for the availability date
        """
        return fields.Datetime.today() + timedelta(days=90)

    @api.onchange("garden")
    def _onchange_garden(self):
        """
        Update the garden area based on the garden value
        """
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.depends("width", "height")
    def _compute_size(self):
        """
        Compute the size of the property based on its width and height
        """
        for record in self:
            record.size = record.width * record.height

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        """
        Compute the best offer for the property based on its offers
        """
        for record in self:
            record.best_offer = max(record.offer_ids.mapped(
                "price")) if record.offer_ids else 0

    def mark_Available(self):
        """
        Mark the property as Available
        """
        for record in self:
            record.state = "available"
        return True

    def mark_Rented(self):
        """
        Mark the property as Rented
        """
        for record in self:
            record.state = "rented"
        return True

    def mark_Under_Maintenance(self):
        """
        Mark the property as Under Maintenance
        """
        for record in self:
            record.state = "under_maintenance"
        return True

    @api.onchange('offer_ids')
    def _onchange_has_offers(self):
        """
        Update the state of the property based on the offers
        """
        self.state = "offer_received" if self.offer_ids else "new"

    def mark_has_offers(self):
        """
        Mark all records as having offers.
        """
        for record in self:
            record.state = "offer_received"
        return True


class PropertyDocument(models.Model):
    _name = 'property.document'
    _description = 'Property Document'

    name = fields.Char(string='Name')
    property_id = fields.Many2one('property', string='Property')
    document = fields.Binary(string='Document')
