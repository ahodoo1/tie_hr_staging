# -*- coding: utf-8 -*-

from odoo import fields, models


class HrEmployee(models.Model):
    """Inheriting hr.employee model for adding fields"""
    _inherit = 'hr.employee'

    resign_date = fields.Date(string="Resign Date", readonly=True,
                              help="Date of the resignation")
    resigned = fields.Boolean(string="Resigned", default=False, store=True,
                              help="If checked then employee has resigned")
    fired = fields.Boolean(string="Fired", default=False, store=True,
                           help="If checked then employee has fired")
