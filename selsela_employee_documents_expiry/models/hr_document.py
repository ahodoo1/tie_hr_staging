# -*- coding: utf-8 -*-

from odoo import fields, models


class HrDocument(models.Model):
    """Store the details of employee documents"""
    _name = 'hr.document'
    _description = 'Documents Template '

    name = fields.Char(string='Document Name', required=True, copy=False,
                       help='You can give your Document name here')
    note = fields.Text(string='Note', copy=False,
                       help="Note for document template")
    attach_ids = fields.Many2many(comodel_name='ir.attachment',
                                  relation='attach_rel_ids', column1='doc_id',
                                  column2='attach_id3', string="Attachment",
                                  help='You can attach the copy of your '
                                       'document', copy=False)
