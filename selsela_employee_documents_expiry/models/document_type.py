# -*- coding: utf-8 -*-

from odoo import fields, models


class DocumentType(models.Model):
    """This model add details of document type"""
    _name = 'document.type'
    _description = "Document Type"

    name = fields.Char(string="Name", required=True,
                       help="Name of the document type")
