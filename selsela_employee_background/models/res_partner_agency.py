# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartnerAgency(models.Model):
    """Inheriting res_partner to add new fields"""
    _inherit = 'res.partner'

    verification_agent = fields.Boolean(string='Employee Verification agent',
                                        default=False,
                                        help="Mark it if the partner is "
                                             "an Employee Verification Agent")
