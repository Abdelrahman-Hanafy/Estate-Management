from datetime import timedelta
from odoo import models, fields, api


class PropertyOffer(models.Model):
    """
    Offer to rent a property.
    """
    _name = 'property.offer'
    _sql_constraints = [
        ('price_positive_check', "CHECK (price >= 0)", 'Price must be positive.'),
    ]

    # price of the offer
    price = fields.Float(string='Price', required=True,
                         help="Price of the offer in€")
    # state of the offer
    state = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='pending', string='State', help="State of the offer")

    # validity of the offer in days
    validity = fields.Integer(string='Validity (days)',
                              default=7, help="Validity of the offer in days")

    #  A computed field defined as the sum of two fields: create_date, validity
    date_deadline = fields.Date(
        string='Deadline', compute="_compute_date_deadline",
        inverse="_set_date_deadline", store=True, help="Deadline of the offer"
    )

    # Start of relational fields
    ########################################################################

    # The property to rent
    property_id = fields.Many2one(
        'property', string='Property', required=True, help="Property to rent")
    # The tenant who made the offer
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True, help="Tenant who made the offer")

    ########################################################################

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        """
        Compute the deadline of the offer based on the validity and creation date.
        """
        for record in self:
            record.date_deadline = (record.create_date or fields.Datetime.today()) + \
                timedelta(days=record.validity)

    def _set_date_deadline(self):
        """
        Update the validity of the offer when the deadline is modified.
        """
        for record in self:
            record.validity = (
                fields.Datetime.to_datetime(record.date_deadline) - (record.create_date or fields.Datetime.today())).days

    def accept_offer(self):
        """
        Accept the offer and mark the property as rented.
        """
        for record in self:
            record.state = 'accepted'
            record.property_id.mark_Rented()
        return True

    def refuse_offer(self):
        """
        Refuse the offer and leave the property available.
        """
        for record in self:
            record.state = 'refused'
        return True
