# -*- coding: utf-8 -*-

from odoo import fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    entry_checklist_plan_ids = fields.Many2many('employee.checklist',
                                                'check_hr_rel', 'hr_check_rel',
                                                string='Entry Process',
                                                domain=[('document_type', '=',
                                                         'entry')],
                                                help="Entry Checklist's")
    exit_checklist_plan_ids = fields.Many2many('employee.checklist',
                                               'exit_hr_rel',
                                               'hr_exit_rel',
                                               string='Exit Process',
                                               domain=[
                                                   ('document_type', '=',
                                                    'exit')],
                                               help="Exit Checklist's")
    check_type_check = fields.Boolean(string="Activity Type Check")
    on_board_type_check = fields.Boolean(string="Onboarding")
    off_board_type_check = fields.Boolean(string="Off-boarding")

    def action_close_dialog(self):
        """
        Function is used for writing checklist values based on
        mail activity of the employee.
        """
        emp_checklist = self.env['hr.employee'].search(
            [('id', '=', self.res_id)])
        emp_checklist.write({
            'entry_checklist': self.entry_checklist_plan_ids if self.entry_checklist_plan_ids else emp_checklist.entry_checklist,
            'exit_checklist': self.exit_checklist_plan_ids if self.exit_checklist_plan_ids else emp_checklist.exit_checklist
        })
        return super().action_close_dialog()
