from odoo import models, fields


class Visitor(models.Model):
    _name = 'property.visitor'
    _description = 'Visitor who visits the property'

    """
    Visitor who visits the property.

    This model represents a visitor who visits a property. A visitor can have
    a purpose (e.g. to find a tenant, to make an offer, etc.) and a state
    (e.g. new, pending, approved, declined, canceled, done) of their visit.
    """

    name = fields.Char(string='Name', help="Name of the visitor")
    mail = fields.Char(string='Email', help="Email of the visitor")
    mobile = fields.Char(string='Mobile', size=11,
                         help="Mobile number of the visitor")

    purpose = fields.Selection([
        ('tenant', 'Tenant'),
        ('buyer', 'Buyer'),
        ('other', 'Other'),
    ], string='Purpose', help="Purpose of the visitor")

    visit_time = fields.Datetime(string='Visit Time',
                                 help="Time when the visitor visited the property")
    state = fields.Selection([
        ('new', 'New'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('canceled', 'Canceled'),
        ('done', 'Done'),
    ], default='new', string='State',
        help="State of the visitor's visit")

    property_id = fields.Many2one('property', string='Property',
                                  help="The property visited by the visitor")
