# -*- coding: utf-8 -*-

from odoo import fields, models


class IrAttachment(models.Model):
    """Add fields on the inherited model ir attachment"""
    _inherit = 'ir.attachment'

    doc_attach_rel_ids = fields.Many2many(comodel_name='hr.employee.document',
                                          relation='doc_attachment_ids',
                                          column1='attach_id3',
                                          column2='doc_id',
                                          string="Attachment",
                                          help="Attachment.",
                                          invisible=1)
    attach_rel_ids = fields.Many2many(comodel_name='hr.document',
                                      relation='attach_ids',
                                      column1='attachment_id3',
                                      column2='document_id',
                                      string="Attachment",
                                      help="Attachments.",
                                      invisible=1)
