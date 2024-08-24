# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    notice_period = fields.Boolean(string='Notice Period',
                                   help="Provide Notice Period for Employees")
    no_of_days = fields.Integer(strig="Notice period days",
                                help="Number of Days of Notice Period")

    def set_values(self):
        """ Setting notice period days to config_settings """
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            "hr_resignation.notice_period", self.notice_period)
        self.env['ir.config_parameter'].sudo().set_param(
            "hr_resignation.no_of_days", self.no_of_days)

    @api.model
    def get_values(self):
        """ Getting notice period days from config_settings """
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['notice_period'] = get_param('hr_resignation.notice_period')
        res['no_of_days'] = int(get_param('hr_resignation.no_of_days'))
        return res
