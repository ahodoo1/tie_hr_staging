# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EmployeeMasterInherit(models.Model):
    _inherit = 'hr.employee'

    @api.depends('exit_checklist')
    def exit_progress(self):
        """This is used to determine the exit status"""
        for each in self:
            total_len = self.env['employee.checklist'].search_count(
                [('document_type', '=', 'exit')])
            entry_len = len(each.exit_checklist)
            if total_len != 0:
                each.exit_progress = (entry_len * 100) / total_len

    @api.depends('entry_checklist')
    def entry_progress(self):
        """This is used to determine the entry status"""
        for each in self:
            total_len = self.env['employee.checklist'].search_count(
                [('document_type', '=', 'entry')])
            entry_len = len(each.entry_checklist)
            if total_len != 0:
                each.entry_progress = (entry_len * 100) / total_len

    entry_checklist = fields.Many2many('employee.checklist', 'entry_obj',
                                       'check_hr_rel', 'hr_check_rel',
                                       string='Entry Process',
                                       domain=[('document_type', '=', 'entry')],
                                       help="Entry Checklist's")
    exit_checklist = fields.Many2many('employee.checklist', 'exit_obj',
                                      'exit_hr_rel', 'hr_exit_rel',
                                      string='Exit Process',
                                      domain=[('document_type', '=', 'exit')],
                                      help="Exit Checklists")
    entry_progress = fields.Float(compute=entry_progress, string='Entry '
                                                                 'Progress',
                                  store=True, default=0.0,
                                  help="Percentage of Entry Checklist's")
    exit_progress = fields.Float(compute=exit_progress, string='Exit Progress',
                                 store=True, default=0.0,
                                 help="Percentage of Exit Checklist's")
    maximum_rate = fields.Integer(default=100)
    check_list_enable = fields.Boolean(invisible=True, copy=False)
