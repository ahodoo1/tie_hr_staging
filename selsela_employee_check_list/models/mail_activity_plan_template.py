# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class MailActivityPlanTemplate(models.Model):
    _inherit = 'mail.activity.plan.template'

    entry_checklist_plan_ids = fields.Many2many('employee.checklist',
                                                'entry_obj_plan',
                                                'check_hr_rel',
                                                'hr_check_rel',
                                                string='Entry Process',
                                                domain=[('document_type', '=',
                                                         'entry')])
    exit_checklist_plan_ids = fields.Many2many('employee.checklist',
                                               'exit_obj_plan', 'exit_hr_rel',
                                               'hr_exit_rel',
                                               string='Exit Process',
                                               domain=[
                                                   ('document_type', '=',
                                                    'exit')])

    def unlink(self):
        """
        Function is used for while deleting the planing types
        it check if the record is related to checklist and raise
        error.

        """
        check_id = self.env.ref(
            'selsela_employee_check_list.checklist_activity_type')
        for recd in self:
            if recd.id == check_id.id:
                raise UserError(_("Checklist Record Can't Be Delete!"))
        return super().unlink()
