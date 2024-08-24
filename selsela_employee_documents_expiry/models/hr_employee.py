# -*- coding: utf-8 -*-

from odoo import fields, models, _


class HrEmployee(models.Model):
    """This class adds number of document on hr employee"""
    _inherit = 'hr.employee'

    def _compute_document_count(self):
        """Compute the number of counts of employee documents"""
        for each in self:
            document_ids = self.env['hr.employee.document'].sudo().search(
                [('employee_ref_id', '=', each.id)])
            each.document_count = len(document_ids)

    def action_document_view(self):
        """Detailed view of employee document"""
        self.ensure_one()
        domain = [('employee_ref_id', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'hr.employee.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_employee_ref_id': %s}" % self.id
        }

    document_count = fields.Integer(compute='_compute_document_count',
                                    string='# Documents',
                                    help="Number of documents of employee")
