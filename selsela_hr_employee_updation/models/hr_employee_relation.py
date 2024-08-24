# -*- coding: utf-8 -*-

from odoo import fields, models


class HrRelationRelation(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.relation'
    _description = "Hr Employee Relation"

    name = fields.Char(string="Relationship",
                       help="Relationship with the employee")
