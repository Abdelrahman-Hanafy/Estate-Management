from odoo import models, fields, api


class PropertyMaintanance(models.Model):
    _name = 'property.maintanance'
    _description = 'Property Maintanance'

    # Request Fields
    name = fields.Char(string='Name')
    maintenance_type = fields.Selection([
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('inspection', 'Inspection'),
    ], string='Type')
    description = fields.Text(string='Description')

    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], default='pending', string='State')

    # Maintanance Fields
    cost = fields.Integer(
        string='Cost', help='Total Cost of the maintenance', default=0)
    start_date = fields.Date(
        string='Start Date', help='Start date of the maintenance')
    duration = fields.Integer(string='Duration', help='Duration in workdays')

    # Relationship Fields
    property_id = fields.Many2one(
        'property', string='Property', default=lambda self: self.env.context.get('property_id', None))

    @api.onchange('cost')
    def _onchange_cost(self):
        if self.cost > 0:
            self.state = 'in_progress'
