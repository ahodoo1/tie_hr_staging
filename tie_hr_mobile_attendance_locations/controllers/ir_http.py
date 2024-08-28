import odoo
from odoo import models
from odoo.http import request
import hashlib
import json
import jwt
from odoo import api, models

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res= super(IrHttp, self).session_info()
        print("Session info",res)
        if res and res.get('uid', False):

                    uid = res.get('uid', False)
                    user_id = self.env["res.users"].sudo().browse(uid)
                    employee_env = self.env["hr.employee"].sudo()
                    token = False
                    employee_id = employee_env.search([('user_id.id', '=', user_id.id)], limit=1)
                    if employee_id:
                        payload = {
                            'employee_id': employee_id.id,
                            'exp': int(
                                self.env['ir.config_parameter'].sudo().get_param('attendance.mobile_expiry_period',
                                                                                    False))
                        }
                        token = jwt.encode(payload, "123tie123@123tie123", algorithm='HS256')

                    image_url = '/web/image?model=res.users&id=%d&field=image_1920' % user_id.id

                    res = {
                        'status': True,
                        'message': 'User login successfully',
                        'user': {
                            'token': token,
                            'user_id': uid,
                            'email': user_id.login,
                            'name': user_id.name,
                            'created_at': user_id.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'updatd_at': user_id.write_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'avatar': "http://localhost:8017" + image_url
                        },
                    }
        return res
