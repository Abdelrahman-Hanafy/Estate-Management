from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from collections import Counter


class ContractManagement(models.Model):
    """
    This class is used to manage contracts between a buyer and a seller.
    A contract is generated by creating a new contract record.
    """
    _name = 'contract.management'
    _description = 'Contract Management'

    name = fields.Char(
        string="Name", default=lambda self: self.env.context.get('name', ''),
        help="Name of the contract")
    duration = fields.Integer(string="Duration in Months", default=1,
                              help="Duration of the contract in months")
    start_date = fields.Date(string="Start Date", default=fields.Date.today(),
                             help="Start date of the contract")
    end_date = fields.Date(string="End Date", compute="_compute_end_date",
                           help="End date of the contract", store=True)

    # Start of relational fields
    ########################################################################

    clauses_ids = fields.Many2many(
        'contract.clause', string="Clauses",
        help="List of clauses included in the contract")
    offer_id = fields.Many2one('property.offer', string="Offer",
                               default=lambda self: self.env.context.get(
                                   'offer_id', None),
                               help="Offer related to the contract")

    # Start of Report fields
    ########################################################################

    avg_duration = fields.Integer(compute="_compute_avg_duration")
    most_used_clause_name = fields.Char(
        compute="_compute_most_used_clause_name"
    )

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):

        for rec in self:
            rec.end_date = rec.start_date + \
                relativedelta(months=rec.duration)

    @api.depends('duration')
    def _compute_avg_duration(self):

        value = sum((rec.duration for rec in self.search([]))) / \
            (self.search_count([]) or 1)

        for rec in self:
            rec.avg_duration = value

    @api.depends('clauses_ids')
    def _compute_most_used_clause_name(self):
        clause_counts = Counter()
        for rec in self:
            clause_counts.update(rec.clauses_ids.mapped('name'))

        # Find clause with the highest count (handle ties)
        most_used_clause = clause_counts.most_common(1)

        for rec in self:
            # Store results
            rec.most_used_clause_name = most_used_clause[0][0] if most_used_clause else None


class Clause(models.Model):
    """
    This model is used to represent clauses included in a contract.
    """
    _name = 'contract.clause'
    _description = 'Contract Clause'

    name = fields.Char(
        'Clause Name', required=True,  # Clause name, e.g. "Rent payment"
        help="Name of the clause included in the contract")
    description = fields.Text(
        'Description',  # Description of the clause
        help="Description of the clause, includes all the details needed")

    # Start of relational fields
    ########################################################################
    contract_id = fields.Many2many(
        'contract.management', string="Contract",  # Contract the clause belongs to
        help="Contract the clause is included in")
