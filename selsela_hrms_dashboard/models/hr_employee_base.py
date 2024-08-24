# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields


class HrEmployeeBase(models.AbstractModel):
    """Inherits the model hr.employee.base to override the
     method _compute_newly_hired"""
    _inherit = 'hr.employee.base'

    def _compute_newly_hired(self):
        """
            Compute the 'newly_hired' field for employees based on the new hire
            date.This method calculates the 'newly_hired' field value for each
            employee by comparing their new hire date with a threshold date
            (90 days ago).
        :return: None
        """
        new_hire_field = self._get_new_hire_field()
        new_hire_date = fields.Datetime.now() - timedelta(days=90)
        for employee in self:
            employee.newly_hired = employee[
                                       new_hire_field] > new_hire_date.date()
