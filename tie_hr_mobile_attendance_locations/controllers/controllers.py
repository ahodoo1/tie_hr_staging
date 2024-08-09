import datetime
import json
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, MissingError, AccessError
import logging

_logger = logging.getLogger(__name__)


class AttendanceLocationController(http.Controller):
    @http.route('/attendance/location', type='json', auth='user', csrf=False)
    def get_emp_attendance_location(self, employee_id, latitude, longitude, attendance_time):
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            attendance_time = datetime.datetime.strptime(attendance_time, '%Y-%m-%d %H:%M:%S')
            attendance_record = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee_id), ('check_in', '!=', False), ('check_out', '=', False)],
                order='id desc', limit=1)
            if attendance_record:
                attendance_data = {
                    'check_out': attendance_time,
                    'check_out_latitude': latitude,
                    'check_out_longitude': longitude,
                    'location_record': True,
                }
                attendance_record.sudo().write(attendance_data)
                res = {'check_out': attendance_record.check_out}
            else:
                attendance_data = {
                    'employee_id': employee_id,
                    'check_in': attendance_time,
                    'check_in_latitude': latitude,
                    'check_in_longitude': longitude,
                    'location_record': True,
                }
                attendance_record = request.env['hr.attendance'].sudo().create(attendance_data)
                res = {'check_in': attendance_record.check_in}
            res.update({
                'response_code': 200,
                'message': 'Submitted Successfully'
            })

        except ValidationError as e:
            request._handle_exception(e)
            res = {
                'response_code': 400,
                'error': str(e)
            }
        except Exception as e:
            res = {
                'response_code': 404,
                'error': str(e)
            }
        return res
