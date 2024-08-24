# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResUsers(models.Model):
    """ Inherit res users for adding fields """
    _inherit = 'res.users'

    employee_id = fields.Many2one(comodel_name='hr.employee',
                                  string='Related Employee',
                                  ondelete='restrict', auto_join=True,
                                  help='Employee-related data of the user')

    @api.model
    def create(self, vals):
        """ This code is to create an employee while creating a user. """
        result = super(ResUsers, self).create(vals)
        val = self.search([('share', '=', False)])
        for record in val:
            if result.id == record.id:
                result['employee_id'] = self.env['hr.employee'].sudo().create(
                    {
                        'name': result['name'],
                        'user_id': result['id'],
                        'private_street': result['partner_id'].name
                    })
        return result
