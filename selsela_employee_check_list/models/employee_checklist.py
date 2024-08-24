# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeChecklist(models.Model):
    _name = 'employee.checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Employee Documents"
    _order = 'sequence'

    name = fields.Char(string='Name', copy=False, required=1,
                       help="Checklist Name")
    document_type = fields.Selection([('entry', 'Entry Process'),
                                      ('exit', 'Exit Process'),
                                      ('other', 'Other')],
                                     string='Checklist Type',
                                     help='Type of Checklist',
                                     required=1)
    sequence = fields.Integer(string='Sequence', help="Sequence of Checklist")
    entry_obj = fields.Many2many('hr.employee', 'entry_checklist',
                                 'hr_check_rel', 'check_hr_rel',
                                 invisible=1, string="Entry Object")
    exit_obj = fields.Many2many('hr.employee', 'exit_checklist', 'hr_exit_rel',
                                'exit_hr_rel', string="Exit Object",
                                invisible=1)
    entry_obj_plan = fields.Many2many('hr.employee', 'entry_checklist_plan_ds',
                                      'hr_check_rel', 'check_hr_rel',
                                      invisible=1, string="Plan Object")
    exit_obj_plan = fields.Many2many('hr.employee', 'exit_checklist_plan_ids',
                                     'hr_exit_rel', 'exit_hr_rel',
                                     invisible=1, string='Exit Plan Object')
