import secrets
from odoo import models, fields, api
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = 'res.users'

    api_token = fields.Char(string='API Token', readonly=True)

    @api.model
    def create(self, vals):
        # Generate API token on user creation
        vals['api_token'] = secrets.token_hex(16)
        return super(ResUsers, self).create(vals)


    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        """Override to assign api_token upon successful login."""
        uid = super(ResUsers, cls).authenticate(db, login, password, user_agent_env)

        if uid:
            # Get the database registry and open a new cursor
            registry = cls.pool
            with registry.cursor() as cr:
                # Create a new environment using the cursor and the authenticated user ID
                env = api.Environment(cr, uid, {})

                # Get the user record
                user = env['res.users'].browse(uid)

                # Check if the user already has an api_token, if not generate one
                if not user.api_token:
                    api_token = secrets.token_hex(16)
                    print(api_token)# Generate a new API token
                    user.api_token = api_token
                    user.write({'api_token': api_token})  # Save the token to the database

        return uid