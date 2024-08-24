# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Inherited res config settings to add the alias prefix and alias
    domain."""
    _inherit = 'res.config.settings'

    alias_prefix = fields.Char(string='Prefix',
                               help='Default alias name for leave',
                               translate=True,
                               config_parameter='hr_holidays.alias_prefix')
    alias_domain = fields.Char(string='Domain', translate=True,
                               help='Default alias domain for leave',
                               config_parameter='hr_holidays.alias_domain')
