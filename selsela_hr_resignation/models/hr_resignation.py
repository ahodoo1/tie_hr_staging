# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

RESIGNATION_TYPE = [('resigned', 'Normal Resignation'),
                    ('fired', 'Fired by the company')]


class HrResignation(models.Model):
    """Model for storing employee resignation details"""
    _name = 'hr.resignation'
    _description = "Create Model for Employee Resignation"
    _inherit = 'mail.thread'
    _rec_name = 'employee_id'

    name = fields.Char(string='Order Reference', required=True, copy=False,
                       readonly=True, index=True,
                       default=lambda self: _('New'))
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee",
                                  default=lambda
                                      self: self.env.user.employee_id.id,
                                  help='Name of the employee for whom the '
                                       'request is creating')
    department_id = fields.Many2one(comodel_name='hr.department',
                                    string="Department",
                                    related='employee_id.department_id',
                                    help='Department of the employee')
    resign_confirm_date = fields.Date(string="Confirmed Date",
                                      help='Date on which the request is '
                                           'confirmed by the employee.',
                                      track_visibility="always")
    approved_revealing_date = fields.Date(
        string="Approved Last Day Of Employee",
        help='Date on which the request is confirmed by the manager.',
        track_visibility="always")
    joined_date = fields.Date(string="Join Date", store=True,
                              help='Joining date of the employee.i.e Start '
                                   'date of the first contract')
    expected_revealing_date = fields.Date(string="Last Day of Employee",
                                          required=True,
                                          help='Employee requested date on '
                                               'which he is revealing from '
                                               'the company.')
    reason = fields.Text(string="Reason", required=True,
                         help='Specify reason for leaving the company')
    notice_period = fields.Char(string="Notice Period")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'),
         ('approved', 'Approved'),
         ('cancel', 'Rejected')],
        string='Status', default='draft', track_visibility="always")
    resignation_type = fields.Selection(selection=RESIGNATION_TYPE,
                                        help="Select the type of "
                                             "resignation: normal"
                                             "resignation or fired by the "
                                             "company")
    read_only = fields.Boolean(string="check field",
                               help="Permission for changing the employee")
    employee_contract = fields.Char(string="Contract",
                                    help="Contract of the selected employee")

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """To get employee joining date"""
        self.joined_date = self.employee_id.joining_date

    @api.model
    def create(self, vals):
        """Assigning the sequence for the record"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'hr.resignation') or _('New')
        res = super(HrResignation, self).create(vals)
        return res

    @api.constrains('employee_id')
    def check_employee(self):
        """Checking whether the user is creating leave request of his/her
           own"""
        for rec in self:
            if not self.env.user.has_group('hr.group_hr_user'):
                if (rec.employee_id.user_id.id and rec.employee_id.user_id.id !=
                        self.env.uid):
                    raise ValidationError(
                        _('You cannot create request for other employees'))

    @api.onchange('employee_id')
    def _onchange_employee_id_request_existence(self):
        """Check whether any resignation request already exists"""
        for rec in self:
            if rec.employee_id:
                resignation_request = self.env['hr.resignation'].search(
                    [('employee_id', '=', rec.employee_id.id),
                     ('state', 'in', ['confirm', 'approved'])])
                if resignation_request:
                    raise ValidationError(
                        _('There is a resignation request in confirmed or'
                          ' approved state for this employee'))
                no_of_contract = self.env['hr.contract'].search(
                    [('employee_id', '=', self.employee_id.id)])
                for contracts in no_of_contract:
                    if contracts.state == 'open':
                        rec.employee_contract = contracts.name
                        rec.notice_period = contracts.notice_days

    def action_confirm_resignation(self):
        """Confirm the resignation request"""
        if self.joined_date:
            if self.joined_date >= self.expected_revealing_date:
                raise ValidationError(
                    _('Last date of the Employee must be anterior to '
                      'Joining date'))
            for rec in self:
                rec.state = 'confirm'
                rec.resign_confirm_date = str(datetime.now())
        else:
            raise ValidationError(_('Please set joining date for employee'))

    def action_cancel_resignation(self):
        """For canceling the resignation request"""
        self.state = 'cancel'

    def action_reject_resignation(self):
        """For rejecting the resignation request"""
        self.state = 'cancel'

    def action_reset_to_draft(self):
        """For setting the resignation request in to draft"""
        for rec in self:
            rec.state = 'draft'
            rec.employee_id.active = True
            rec.employee_id.resigned = False
            rec.employee_id.fired = False

    def action_approve_resignation(self):
        """For approving the resignation request"""
        for rec in self:
            if rec.expected_revealing_date and rec.resign_confirm_date:
                no_of_contract = self.env['hr.contract'].search(
                    [('employee_id', '=', self.employee_id.id)])
                for contracts in no_of_contract:
                    if contracts.state == 'open':
                        rec.employee_contract = contracts.name
                        rec.state = 'approved'
                        rec.approved_revealing_date = (rec.resign_confirm_date +
                                                       timedelta(
                            days=contracts.notice_days))
                    else:
                        rec.approved_revealing_date = (
                            rec.expected_revealing_date)
                # Changing state of the employee if resigning today
                if (rec.expected_revealing_date <= fields.Date.today() and
                        rec.employee_id.active):
                    rec.employee_id.active = False
                    # Changing fields in the employee table with respect to
                    # resignation
                    rec.employee_id.resign_date = rec.expected_revealing_date
                    if rec.resignation_type == 'resigned':
                        rec.employee_id.resigned = True
                    else:
                        rec.employee_id.fired = True
                    # Removing and deactivating user
                    if rec.employee_id.user_id:
                        rec.employee_id.user_id.active = False
                        rec.employee_id.user_id = None
            else:
                raise ValidationError(_('Please enter valid dates.'))

    def update_employee_status(self):
        """Removing and deactivating user"""
        resignation = self.env['hr.resignation'].search(
            [('state', '=', 'approved')])
        for rec in resignation:
            if (rec.expected_revealing_date <= fields.Date.today() and
                    rec.employee_id.active):
                rec.employee_id.active = False
                # Changing fields in the employee table with respect to
                # resignation
                rec.employee_id.resign_date = rec.expected_revealing_date
                if rec.resignation_type == 'resigned':
                    rec.employee_id.resigned = True
                else:
                    rec.employee_id.fired = True
                if rec.employee_id.user_id:
                    rec.employee_id.user_id.active = False
                    rec.employee_id.user_id = None
