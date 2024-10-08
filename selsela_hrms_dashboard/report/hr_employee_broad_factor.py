# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models


class HrEmployeeBroadFactor(models.Model):
    _name = "hr.employee.broad.factor"
    _description = "Employee Broad factor"
    _auto = False

    name = fields.Char(string="Name", help="Name of factor")
    no_of_occurrence = fields.Integer(string="Number of Occurrence",
                                      help="Number of Occurrence of factor")
    no_of_days = fields.Integer(string="Number of Days", help="Number of Days")
    broad_factor = fields.Integer(string="Broad Factor", help="Broad Factor")

    def init(self):
        """
            Initialize the module and create or replace the
            'hr_employee_broad_factor' view. This method drops the existing
            view if it exists and creates a new view that calculates
            the broad factor for each employee based on their leave records.
            The 'hr_employee_broad_factor' view includes the following columns:
            - id: Employee ID
            - name: Employee name
            - no_of_occurrence: Number of leave occurrences for the employee
            - no_of_days: Total number of leave days for the employee
            - broad_factor: A calculated broad factor using the formula:
                            (no_of_occurrence * no_of_occurrence * no_of_days)
            This method should be called during the initialization of the
            module to ensure the 'hr_employee_broad_factor' view is up-to-date.
        """
        tools.drop_view_if_exists(self._cr, 'hr_employee_broad_factor')
        self._cr.execute("""
            create or replace view hr_employee_broad_factor as (
                select
                    e.id, e.name, count(h.*) as no_of_occurrence,
                    sum(h.number_of_days) as no_of_days,
                    count(h.*)*count(h.*)*sum(h.number_of_days) as broad_factor
                from hr_employee e
                    full join (select * from hr_leave where state = 'validate' 
                    and date_to <= now()::timestamp) h
                    on e.id =h.employee_id
                group by e.id
               )""")


class ReportBroadFactor(models.AbstractModel):
    _name = 'report.hrms_dashboard.report_broadfactor'

    @api.model
    def get_report_values(self, docids=None, data=None):
        """ Get report of broad factor. """
        sql = """select * from hr_employee_broad_factor"""
        self.env.cr.execute(sql)
        lines = self.env.cr.dictfetchall()
        return {
            'doc_model': 'hr.employee.broad_factor',
            'lines': lines,
            'Date': fields.date.today(),
        }
