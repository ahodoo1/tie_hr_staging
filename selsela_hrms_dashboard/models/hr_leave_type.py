# -*- coding: utf-8 -*-

from odoo import fields, models


class HrLeaveType(models.Model):
    """
        This class extends the 'hr.leave.type' model in Odoo to add a
        custom field.
        Attributes:
            _inherit (str): Indicates the model to be extended.
        Fields:
            emp_broad_factor (Boolean): A custom boolean field added to the
            'hr.leave.type' model.
    """
    _inherit = 'hr.leave.type'

    emp_broad_factor = fields.Boolean(
        string="Broad Factor", help="It will display in broad factor type")
