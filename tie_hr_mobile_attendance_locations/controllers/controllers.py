import datetime
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from odoo import http
from odoo.http import request
import logging
import json
import pytz

_logger = logging.getLogger(__name__)


class AttendanceLocationController(http.Controller):
    @http.route('/attendance/location', type='json', auth='user', csrf=False)
    def get_emp_attendance_location(self):
        try:
            # Fetch Data Payload
            data = request.httprequest.data.decode()
            vals = json.loads(data)
            jwt_token = request.httprequest.headers.get('jwt_token')
            accept_language = request.httprequest.headers.get('Accept-Language')
            decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})

            # Validation Layer
            if not vals.get('tz', False):
                return {
                    'status': False,
                    'message': 'Timezone(tz) is required' if accept_language != 'ar' else 'المنطقة الزمنية مطلوبه'
                }
            if not vals.get('latitude', False):
                return {
                    'status': False,
                    'message': 'Latitude(latitude) is required' if accept_language != 'ar' else 'خط العرض مطلوب'
                }
            if not vals.get('longitude', False):
                return {
                    'status': False,
                    'message': 'Longitude(longitude) is required' if accept_language != 'ar' else 'خط الطول مطلوب'
                }

            if not vals.get('attendance_time', False):
                return {
                    'status': False,
                    'message': 'Attendance Time(attendance_time) is required' if accept_language != 'ar' else 'وقت الحضور مطلوب'
                }
            # Token Authorization
            if not jwt_token:
                return {
                    'status': False,
                    'message': 'Authorization Header Missing' if accept_language else 'الرمز مفقود'
                }

            if "employee_id" not in decoded_token:
                return {
                    'status': False,
                    'message': 'Invalid Token' if accept_language != 'ar' else 'رمز غير صالح'
                }

            employee_id = decoded_token.get("employee_id")
            latitude = float(vals.get("latitude"))
            longitude = float(vals.get("longitude"))
            expiry_period_minutes = decoded_token.get("exp")

            if expiry_period_minutes:
                expiry_period_minutes = float(expiry_period_minutes)  # Ensure it's a float

            emp_id = request.env["hr.employee"].sudo().search([("id", "=", employee_id)])
            if not emp_id:
                return {
                    'status': False,
                    'message': 'Employee Not Found' if accept_language != 'ar' else 'الموظف غير متوفر'
                }
            # Retrieve employee's time zone
            employee_tz_name = emp_id.tz or 'UTC'  # Default to UTC if no time zone is set
            payload_tz = vals.get('tz')
            try:
                payload_timezone = pytz.timezone(payload_tz)
                employee_timezone = pytz.timezone(employee_tz_name)
            except pytz.UnknownTimeZoneError:
                return {
                    'status': False,
                    'message': 'Invalid Time Zone' if accept_language != 'ar' else 'منظقه زمنيه غير صالحه'
                }
            # Convert attendance time from payload timezone to UTC
            attendance_time = datetime.datetime.strptime(vals.get("attendance_time"), '%Y-%m-%d %H:%M:%S')
            attendance_time_localized = payload_timezone.localize(attendance_time)
            attendance_time_utc = attendance_time_localized.astimezone(pytz.utc)
            # Calculate expiration window
            current_time = datetime.datetime.now(pytz.utc)
            expiration_time = attendance_time_utc + datetime.timedelta(minutes=expiry_period_minutes)

            if current_time > expiration_time:
                return {
                    'status': False,
                    'message': 'Session has expired. Please log in again.' if accept_language != 'ar' else 'انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى'
                }

            # Convert UTC time to employee's timezone
            attendance_time_in_employee_tz = attendance_time_utc.astimezone(employee_timezone)

            # Convert to naive datetime (remove timezone info) for storing in Odoo
            naive_attendance_time = attendance_time_in_employee_tz.replace(tzinfo=None)

            attendance_record = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee_id), ('check_in', '!=', False),
                ('check_out', '=', False)],
                order='id desc', limit=1)
            if attendance_record:
                attendance_data = {
                    'check_out': naive_attendance_time,
                    'check_out_latitude': latitude,
                    'check_out_longitude': longitude,
                    'location_record': True,
                }
                attendance_record.sudo().write(attendance_data)
                res = {'check_out': attendance_record.check_out}
            else:
                attendance_data = {
                    'employee_id': employee_id,
                    'check_in': naive_attendance_time,
                    'check_in_latitude': latitude,
                    'check_in_longitude': longitude,
                    'location_record': True,
                }
                attendance_record = request.env['hr.attendance'].sudo().create(attendance_data)
                res = {'check_in': attendance_record.check_in}
            res.update({
                'status': True,
                'message': 'Submitted Successfully' if accept_language != 'ar' else 'تم الارسال بنجاح'
            })

        except ExpiredSignatureError:
            # If the token is expired, handle it here
            res = {
                'status': False,
                'message': 'Token has expired. Please log in again.' if accept_language != 'ar' else 'انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى'
            }
            return res

        except Exception as e:
            res = {
                'status': False,  # Use a more generic error code for unexpected exceptions
                'message': str(e)
            }
            return res

            # Return the successful response if everything is processed correctly
        return res

    @http.route('/api/auth/login', type='json', auth='none')
    def auth_login(self):
        try:
            data = request.httprequest.data.decode()
            vals = json.loads(data)
            accept_language = request.httprequest.headers.get('Accept-Language')

            request.session.authenticate(vals.get('db'), vals.get('login'), vals.get('password'))
            response = request.env['ir.http'].session_info()
            if response and response.get('uid', False):

                uid = response.get('uid')
                user_id = request.env["res.users"].sudo().browse(uid)
                image_url = '/web/image?model=res.users&id=%d&field=image_1920' % user_id.id

                res = {
                    'status': True,
                    'message': 'User login successfully' if accept_language != 'ar' else "تم تسجيل دخول المستخدم بنجاح",
                    'user': {
                        'user_id': uid,
                        'email': user_id.login,
                        'name': user_id.name,
                        'created_at': user_id.create_date,
                        'updatd_at': user_id.write_date,
                        'avatar': "http://localhost:8017"+image_url
                    },
                }
                return res
            else:
                return {
                    'status': False,
                    'message': 'Invalid credentials' if accept_language != 'ar' else "بيانات اعتماد غير صالحة",
                }
        except Exception as e:
            # Handle exceptions
            return {
                'status': False,
                'message': str(e) if accept_language != 'ar' else "بيانات اعتماد غير صالحة",
            }
