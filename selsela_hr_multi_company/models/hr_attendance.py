# -*- coding: utf-8 -*-

from odoo import fields, models


class HrAttendance(models.Model):
    """Adding fields to hr.attendance model"""
    _inherit = 'hr.attendance'

    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 copy=False, readonly=True, help="Company",
                                 default=lambda self: self.env.user.company_id)
