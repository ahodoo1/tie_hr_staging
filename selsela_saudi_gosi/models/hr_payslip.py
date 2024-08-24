# -*- coding: utf-8 -*-

from odoo import fields, api, models, _


class HrPayslip(models.Model):
    """Inherited hr_payslip to add new fields"""
    _inherit = 'hr.payslip'

    gosi_no = fields.Many2one('gosi.payslip',
                              string='GOSI Reference', readonly=True,
                              help="Choose/Create Gosi Number")

    @api.onchange('employee_id')
    def onchange_employee_ref(self):
        """Check Employee and Fetch Gosi Ref"""
        for rec in self:
            gosi_no = rec.env['gosi.payslip'].search(
                [('employee_id', '=', rec.employee_id.id)])
            rec.gosi_no = gosi_no.id
