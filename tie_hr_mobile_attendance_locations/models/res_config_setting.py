# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    attendance_expiry_period  = fields.Integer(string="Expiry Period With minutes", required=True,
                                                          default=30,config_parameter="attendance.mobile_expiry_period")

    @api.constrains('attendance_expiry_period')
    def validate_attendance_expiry_period(self):
        if self.attendance_expiry_period < 0:
            raise ValidationError(_('Expiry Period must be a positive integer.'))
