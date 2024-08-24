# -*- coding: utf-8 -*-

from odoo import fields, models


class ServiceExecution(models.Model):
    """Model to create records for executing the service"""
    _name = 'service.execution'
    _rec_name = 'issue'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'issue'

    client_id = fields.Many2one('hr.employee',
                                string="Client", help="Client")
    executer_id = fields.Many2one('hr.employee',
                                  string='Executer', help="Executer")
    issue = fields.Char(string="Issue", help="Issue")
    execute_date = fields.Datetime(string="Date Of Reporting",
                                   help="Date of reporting")
    state_execute = fields.Selection(
        [('draft', 'Draft'), ('requested', 'Requested'),
         ('assign', 'Assigned'), ('check', 'Checked'), ('reject', 'Rejected'),
         ('approved', 'Approved')], tracking=True, )
    test_id = fields.Many2one('service.request', string='test',
                              help="Test")
    notes = fields.Text(string="Internal notes", help="Internal Notes")
    executer_product = fields.Char(string='Service Item', help="service item")
    type_service = fields.Char(string='Service Type', help="Service type")

    def action_service_check(self):
        """Button Checked"""
        self.test_id.sudo().state = 'check'
        self.write({
            'state_execute': 'check'
        })
        return
