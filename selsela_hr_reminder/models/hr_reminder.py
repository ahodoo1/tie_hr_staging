# -*- coding: utf-8 -*-

from odoo import models, fields


class HrReminder(models.Model):
    """Creates the model Hr Reminder to create the reminders."""
    _name = 'hr.reminder'
    _description = "HR Reminder"

    name = fields.Char(string='Title', required=True,
                       help="Title of the reminder")
    model_id = fields.Many2one(comodel_name='ir.model', help="Choose the model name",
                               string="Model", required=True,
                               ondelete='cascade',
                               domain="[('model', 'like','hr')]")
    field_id = fields.Many2one(comodel_name='ir.model.fields', string='Field',
                               help="Choose the field",
                               domain="[('model_id', '=',model_id),"
                                      "('ttype', 'in', ['datetime','date'])]"
                               , required=True, ondelete='cascade')
    search_by = fields.Selection([('today', 'Today'),
                                  ('set_period', 'Set Period'),
                                  ('set_date', 'Set Date'), ],
                                 required=True, string="Search By",
                                 help="Search by the given field")
    days_before = fields.Integer(string='Reminder before',
                                 help="Number of days before the reminder "
                                      "should show")
    date_set = fields.Date(string='Select Date',
                           help="Select the reminder set date")
    date_from = fields.Date(string="Start Date",
                            help="Start date to show the reminder")
    date_to = fields.Date(string="End Date",
                          help="End date to not show the reminder")
    expiry_date = fields.Date(string="Reminder Expiry Date",
                              help="Expiry date to expires out the reminder")
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 required=True, help="Company of the record",
                                 default=lambda self: self.env.user.company_id)
