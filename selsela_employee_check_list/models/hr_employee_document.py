# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrEmployeeDocument(models.Model):
    _inherit = 'hr.employee.document'

    document_name = fields.Many2one('employee.checklist',
                                    string='Checklist Document',
                                    help='Choose the document in the '
                                         'checklist here.Automatically the '
                                         'checklist box become true')

    @api.model
    def create(self, vals):
        """Supering the create function"""
        result = super().create(vals)
        if result.document_name.document_type == 'entry':
            result.employee_ref.write(
                {'entry_checklist': [(4, result.document_name.id)]})
        if result.document_name.document_type == 'exit':
            result.employee_ref.write(
                {'exit_checklist': [(4, result.document_name.id)]})
        return result

    def unlink(self):
        """Supering the unlink method"""
        for result in self:
            if result.document_name.document_type == 'entry':
                result.employee_ref.write(
                    {'entry_checklist': [(5, result.document_name.id)]})
            if result.document_name.document_type == 'exit':
                result.employee_ref.write(
                    {'exit_checklist': [(5, result.document_name.id)]})
        res = super().unlink()
        return res
