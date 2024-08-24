# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class HrEmployee(models.Model):
    """Inherited hr_employee to add new fields"""
    _inherit = 'hr.employee'

    type = fields.Selection([('saudi', 'Saudi')], string='Type',
                            help="Select the type")
    gosi_number = fields.Char(string='GOSI Number', help="Enter Gosi Number")
    issue_date = fields.Date(string='Issued Date', help="Choose Issued Date")
    age = fields.Char(string='Age', help="Enter Age")
    limit = fields.Boolean(string='Eligible For GOSI', compute='_compute_age',
                           default=False,
                           help="Eligibility for GOSI")

    @api.depends('age')
    def _compute_age(self):
        """Check age for gosi eligibility"""
        for res in self:
            if 60 >= int(res.age) >= 18:
                res.limit = True
            else:
                res.limit = False
