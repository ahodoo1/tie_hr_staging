# -*- coding: utf-8 -*-

from datetime import date
from odoo import fields, models
from odoo.exceptions import UserError


class HrLoan(models.Model):
    """ Inheriting hr.loan for adding fields into the model. """
    _inherit = 'hr.loan'

    employee_account_id = fields.Many2one(comodel_name='account.account',
                                          string="Loan Account",
                                          help="Select employee chart of "
                                               "accounts")
    treasury_account_id = fields.Many2one(comodel_name='account.account',
                                          string="Treasury Account",
                                          help="Select employee treasury "
                                               "account details")
    journal_id = fields.Many2one(comodel_name='account.journal',
                                 string="Journal",
                                 help="Select journal for employee")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange',
        copy=False)

    def action_approve(self):
        """ This creates an invoice in account.move with loan request details.
        """
        loan_approve = self.env['ir.config_parameter'].sudo().get_param(
            'account.loan_approve')
        contract_obj = self.env['hr.contract'].search(
            [('employee_id', '=', self.employee_id.id)])
        if not contract_obj:
            raise UserError('You must Define a contract for employee')
        if not self.loan_line_ids:
            raise UserError('You must compute installment before Approved')
        if loan_approve:
            self.write({'state': 'waiting_approval_2'})
        else:
            if (not self.employee_account_id or not self.treasury_account_id or
                    not self.journal_id):
                raise UserError(
                    "You must enter employee account & Treasury account and"
                    " journal to approve ")
            if not self.loan_line_ids:
                raise UserError(
                    'You must compute Loan Request before Approved')
            for loan in self:
                debit_vals = {
                    'name': loan.employee_id.name,
                    'account_id': loan.treasury_account_id.id,
                    'journal_id': loan.journal_id.id,
                    'date': date.today(),
                    'debit': loan.loan_amount > 0.0 and loan.loan_amount or 0.0,
                    'credit': loan.loan_amount < 0.0 and -loan.loan_amount
                              or 0.0,
                    'loan_id': loan.id,
                }
                credit_vals = {
                    'name': loan.employee_id.name,
                    'account_id': loan.employee_account_id.id,
                    'journal_id': loan.journal_id.id,
                    'date': date.today(),
                    'debit': loan.loan_amount < 0.0 and
                             -loan.loan_amount or 0.0,
                    'credit': loan.loan_amount > 0.0 and
                              loan.loan_amount or 0.0,
                    'loan_id': loan.id,
                }
                vals = {
                    'name': 'Loan For' + ' ' + loan.employee_id.name,
                    'narration': loan.employee_id.name,
                    'ref': loan.name,
                    'journal_id': loan.journal_id.id,
                    'date': date.today(),
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                move = self.env['account.move'].create(vals)
                move.action_post()
            self.write({'state': 'approve'})
        return True

    def action_double_approve(self):
        """ This creates account move for request in case of double approval.
        """
        if (not self.employee_account_id or not self.treasury_account_id or not
        self.journal_id):
            raise UserError(
                "You must enter employee account & Treasury account and "
                "journal to approve ")
        if not self.loan_line_ids:
            raise UserError('You must compute Loan Request before Approved')
        for loan in self:
            debit_vals = {
                'name': loan.employee_id.name,
                'account_id': loan.treasury_account_id.id,
                'journal_id': loan.journal_id.id,
                'date': date.today(),
                'debit': loan.loan_amount > 0.0 and loan.loan_amount or 0.0,
                'credit': loan.loan_amount < 0.0 and -loan.loan_amount or 0.0,
                'loan_id': loan.id,
            }
            credit_vals = {
                'name': loan.employee_id.name,
                'account_id': loan.employee_account_id.id,
                'journal_id': loan.journal_id.id,
                'date': date.today(),
                'debit': loan.loan_amount < 0.0 and -loan.loan_amount or 0.0,
                'credit': loan.loan_amount > 0.0 and loan.loan_amount or 0.0,
                'loan_id': loan.id,
            }
            vals = {
                'name': 'Loan For' + ' ' + loan.employee_id.name,
                'narration': loan.employee_id.name,
                'ref': loan.name,
                'journal_id': loan.journal_id.id,
                'date': date.today(),
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.action_post()
        self.write({'state': 'approve'})
        return True
