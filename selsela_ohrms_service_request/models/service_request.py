# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ServiceRequest(models.Model):
    """Model to create records for employee service requests"""
    _name = 'service.request'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "service_name"

    def _get_employee_id(self):
        """Default employee_id"""
        employee_rec = self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id

    service_name = fields.Char(required=True, string="Reason For Service",
                               help="Service name")
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  default=_get_employee_id, readonly=True,
                                  required=True, help="Employee")
    service_date = fields.Datetime(string="Date", required=True,
                                   help="Service date")
    state = fields.Selection([('draft', 'Draft'),
                              ('requested', 'Requested'),
                              ('assign', 'Assigned'),
                              ('check', 'Checked'),
                              ('reject', 'Rejected'),
                              ('approved', 'Approved')], default='draft',
                             tracking=True, help="State")
    service_executer_id = fields.Many2one('hr.employee',
                                          string='Service Executer',
                                          help="Choose service executer")
    read_only = fields.Boolean(string="check field", compute='get_user')
    tester_ids = fields.One2many('service.execution', 'test_id',
                                 string='tester', help="Tester")
    internal_note = fields.Text(string="internal notes", help="Internal Notes")
    service_type = fields.Selection([('repair', 'Repair'),
                                     ('replace', 'Replace'),
                                     ('updation', 'Updation'),
                                     ('checking', 'Checking'),
                                     ('adjust', 'Adjustment'),
                                     ('other', 'Other')],
                                    string='Type Of Service', required=True,
                                    help="Type for the service request")
    service_product_id = fields.Many2one('product.product',
                                         string='Item For Service',
                                         required=True,
                                         help="Product you want to service")
    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True,
                       default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        """Sequence number"""
        vals['name'] = self.env['ir.sequence'].next_by_code('service.request')
        return super(ServiceRequest, self).create(vals)

    @api.depends('read_only')
    def get_user(self):
        """Fetch user"""
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('project.group_project_manager'):
            self.read_only = True
        else:
            self.read_only = False

    def action_submit_reg(self):
        """Button Submit"""
        self.ensure_one()
        self.sudo().write({
            'state': 'requested'
        })
        return

    def action_assign_executer(self):
        """Button Assign"""
        self.ensure_one()
        if not self.service_executer_id:
            raise ValidationError(
                _("Select Executer For the Requested Service"))
        self.write({
            'state': 'assign'
        })
        vals = {
            'issue': self.service_name,
            'executer_id': self.service_executer_id.id,
            'client_id': self.employee_id.id,
            'executer_product': self.service_product_id.name,
            'type_service': self.service_type,
            'execute_date': self.service_date,
            'state_execute': self.state,
            'notes': self.internal_note,
            'test_id': self.id,
        }
        self.env['service.execution'].sudo().create(vals)

    def action_service_approval(self):
        """Button Approve"""
        for record in self:
            record.tester_ids.sudo().state_execute = 'approved'
            record.write({
                'state': 'approved'
            })
        return

    def action_service_rejection(self):
        """Button Reject"""
        self.write({
            'state': 'reject'
        })
        return
