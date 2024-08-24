# -*- coding: utf-8 -*-

from odoo import fields, models


class HrSalaryRuleCategory(models.Model):
    """Adding fields to hr.salary.rule.category model."""
    _inherit = 'hr.salary.rule.category'

    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 copy=False, readonly=True, help="Company",
                                 default=lambda self: self.env.user.company_id)
