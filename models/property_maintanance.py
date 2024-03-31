from odoo import models, fields, api


class PropertyMaintanance(models.Model):
    _name = 'property.maintanance'
    _description = 'Property Maintanance'

    ##### Request Fields #####
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

    ##### Maintanance Fields #####
    cost = fields.Integer(
        string='Cost', help='Total Cost of the maintenance', default=0)
    start_date = fields.Date(
        string='Start Date', help='Start date of the maintenance')
    duration = fields.Integer(string='Duration', help='Duration in workdays')

    ##### Relationship Fields #####
    property_id = fields.Many2one(
        'property', string='Property', default=lambda self: self.env.context.get('property_id', None))

    #### Actions ####
    def action_start(self):
        self.state = 'in_progress'
        self.property_id.maintenance_state = 'in_progress'
        return True

    def action_done(self):
        self.state = 'done'
        self.property_id.maintenance_state = 'good'
        return True


class PropertyMaintananceRequest(models.TransientModel):

    _name = 'property.maintanance.request'
    _description = 'Maintanance Request'

    name = fields.Char(string='Name')
    maintenance_type = fields.Selection([
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('inspection', 'Inspection'),
    ], string='Type')
    description = fields.Text(string='Description')

    def action_request(self):
        self.ensure_one()
        property = self.env['property'].browse(
            self.env.context.get('active_id'))
        property_maintanance = self.env['property.maintanance'].create({
            'property_id': property.id,
            'name': self.name,
            'maintenance_type': self.maintenance_type,
            'description': self.description
        })

        property.maintenance_state = 'requested'
        return property_maintanance
