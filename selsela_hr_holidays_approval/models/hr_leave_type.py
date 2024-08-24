# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrLeaveType(models.Model):
    """ Extend model to add multilevel approval """
    _inherit = 'hr.leave.type'

    leave_validation_type = fields.Selection(
        selection_add=[('multi', 'Multi Level Approval')])
    leave_validators_ids = fields.One2many('hr.holidays.validators',
                                           'hr_holiday_status_id',
                                           string='Leave Validators',
                                           help="Approval users")

    @api.constrains('leave_validators_ids')
    def check_leave_validators_ids(self):
        """Checking the validation"""
        for each in self:
            if not each.leave_validators_ids \
                    and each.leave_validation_type == 'multi':
                raise UserError(_('You cannot make leave validators empty '
                                  'when selecting Multi Level Approval'))


class HrLeaveValidators(models.Model):
    """ Model for leave validators in Leave Types configuration """
    _name = 'hr.holidays.validators'

    hr_holiday_status_id = fields.Many2one('hr.leave.type',
                                           string="Holiday Status")
    holiday_validators_id = fields.Many2one('res.users',
                                            string='Leave Validators',
                                            help="Leave validators",
                                            domain="[('share','=',False)]")
