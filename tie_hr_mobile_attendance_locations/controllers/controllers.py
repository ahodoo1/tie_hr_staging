import datetime
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import requests
from odoo.http import request, Response
from urllib.parse import parse_qs
import odoo
import json
import pytz

from odoo import http
from odoo.exceptions import AccessError
from passlib.context import CryptContext

# Odoo's context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["pbkdf2_sha512"], deprecated="auto")


class AttendanceLocationController(http.Controller):

    def verify_password(plain_password, hashed_password):
        # Verify the plain password against the stored hashed password
        return pwd_context.verify(plain_password, hashed_password)

    def get_fail_response(self, message):
        result = {
            'status': False,
            'code': 401,
            'message': message
        }
        return result

    @http.route('/web/session/authenticate', type='json', auth='none')
    def authenticate(self, db, login, password, base_location=None):
        accept_language = False
        accept_language = request.httprequest.headers.get('Accept-Language')
        if not http.db_filter([db]):
            # raise AccessError("Database not found.")
            message = "Database not found" if accept_language != 'ar' else 'قاعدة بيانات غير متوفره'
            return self.get_fail_response(message)

        def hash_password(password):
            # Hash the password using the context
            return pwd_context.hash(password)

        hash_password = hash_password(password)
        usr_login = request.env['res.users'].sudo().search([('login', '=', login), ('password', '=', hash_password)])

        if not usr_login:
            message = "Invalid username or password" if accept_language != 'ar' else 'كلمة مرور او مستخدم غير صالح'
            return self.get_fail_response(message)
        pre_uid = request.session.authenticate(db, login, password)
        if pre_uid != request.session.uid:
            return {'uid': None}

        request.session.db = db
        registry = odoo.modules.registry.Registry(db)
        with registry.cursor() as cr:
            env = odoo.api.Environment(cr, request.session.uid, request.session.context)

            # Custom response to return additional user details
            user_id = env['res.users'].sudo().browse(request.session.uid)
            token = False
            image_url = '/web/image?model=res.users&id=%d&field=image_1920' % user_id.id

            response = {
                'status': True,
                'code': 200,
                'message': 'User login successfully' if accept_language != 'ar' else 'تم تسجيل الدخول بنجاح',
                'user': {
                    'token': user_id.api_token,
                    'user_id': request.session.uid,
                    'email': user_id.login,
                    'name': user_id.name,
                    'created_at': user_id.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': user_id.write_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'avatar': "http://localhost:8017" + image_url if image_url else None
                }
            }

            # Update session cookie if necessary
            if not request.db and not request.session.is_explicit:
                http.root.session_store.rotate(request.session, env)
                request.future_response.set_cookie(
                    'session_id', request.session.sid,
                    max_age=http.SESSION_LIFETIME, httponly=True
                )

            return response

    def _is_token_valid(self, token):
        user = request.env['res.users'].sudo().search([('api_token', '=', token)], limit=1)
        return bool(user)

    @http.route('/attendance/location', type='json', auth='none', csrf=False, methods=['POST'])
    def get_emp_attendance_location(self, **kw):
        try:
            # Fetch header data
            accept_language = False
            accept_language = request.httprequest.headers.get('Accept-Language')
            token = request.httprequest.headers.get('token')
            if not token or not self._is_token_valid(token):
                message = 'Invalid Token' if accept_language != 'ar' else 'رمز غير صالح'
                return self.get_fail_response(message)

            # Fetch Data Payload
            tz = kw.get('tz', False)
            latitude = kw.get('latitude', False)
            longitude = kw.get('longitude', False)
            attendance_time = kw.get('attendance_time', "")

            # jwt_token = request.httprequest.headers.get('jwt_token')
            # user_token = request.httprequest.headers.get('token')
            # decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})

            # Validation Layer
            if not tz:
                message = 'Timezone(tz) is required' if accept_language != 'ar' else 'المنطقة الزمنية مطلوبه'
                return self.get_fail_response(message)
            if not latitude:
                message = 'Latitude(latitude) is required' if accept_language != 'ar' else 'خط العرض مطلوب'
                return self.get_fail_response(message)
            if not longitude:
                message = 'Longitude(longitude) is required' if accept_language != 'ar' else 'خط الطول مطلوب'
                return self.get_fail_response(message)

            if not attendance_time:
                message = 'Attendance Time(attendance_time) is required' if accept_language != 'ar' else 'وقت الحضور مطلوب'
                return self.get_fail_response(message)

            # expiry_period_minutes = decoded_token.get("exp")
            # print(expiry_period_minutes)
            #
            # if expiry_period_minutes:
            #     expiry_period_minutes = int(expiry_period_minutes)

            emp_id = request.env["hr.employee"].sudo().search([("user_id.api_token", "=", token)])
            if not emp_id:
                message = 'Invalid Employee' if accept_language != 'ar' else 'الموظف غير متوفر'
                return self.get_fail_response(message)

            # Retrieve employee's time zone
            employee_tz_name = emp_id.tz or 'UTC'  # Default to UTC if no time zone is set
            payload_tz = tz
            try:
                payload_timezone = pytz.timezone(payload_tz)
                employee_timezone = pytz.timezone(employee_tz_name)
            except pytz.UnknownTimeZoneError:
                message = 'Invalid Time Zone' if accept_language != 'ar' else 'منظقه زمنيه غير صالحه'
                return self.get_fail_response(message)
            # Convert attendance time from payload timezone to UTC
            attendance_time = datetime.datetime.strptime(attendance_time, '%Y-%m-%d %H:%M:%S')
            attendance_time_localized = payload_timezone.localize(attendance_time)
            attendance_time_utc = attendance_time_localized.astimezone(pytz.utc)
            # Calculate expiration window
            # current_time = datetime.datetime.now(pytz.utc)
            # expiration_time = attendance_time_utc + datetime.timedelta(minutes=expiry_period_minutes)
            #
            # if current_time > expiration_time:
            #     result = {
            #         'status': False,
            #         'message': 'Session has expired. Please log in again.' if accept_language != 'ar' else 'انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى'
            #     }
            #     return Response(
            #         json.dumps(result),
            #         content_type='application/json',
            #         status=401
            #     )

            # Convert UTC time to employee's timezone
            attendance_time_in_employee_tz = attendance_time_utc.astimezone(employee_timezone)

            # Convert to naive datetime (remove timezone info) for storing in Odoo
            naive_attendance_time = attendance_time_in_employee_tz.replace(tzinfo=None)

            attendance_record = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', emp_id.id), ('check_in', '!=', False),
                ('check_out', '=', False)],
                order='id desc', limit=1)
            if attendance_record:
                attendance_data = {
                    'check_out': str(naive_attendance_time),
                    'check_out_latitude': latitude,
                    'check_out_longitude': longitude,
                    'location_record': True,
                }
                attendance_record.sudo().write(attendance_data)
                res = {'check_out': attendance_record.check_out.strftime('%Y-%m-%d %H:%M:%S')}
            else:
                attendance_data = {
                    'employee_id': emp_id.id,
                    'check_in': naive_attendance_time,
                    'check_in_latitude': latitude,
                    'check_in_longitude': longitude,
                    'location_record': True,
                }
                attendance_record = request.env['hr.attendance'].sudo().create(attendance_data)
                res = {'check_in': attendance_record.check_in.strftime('%Y-%m-%d %H:%M:%S'), }
            res.update({
                'status': True,
                'code': 200,
                'message': 'Submitted Successfully' if accept_language != 'ar' else 'تم الارسال بنجاح'
            })

        except ExpiredSignatureError:
            # If the token is expired, handle it here
            message = 'Token has expired. Please log in again.' if accept_language != 'ar' else 'انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى'
            return self.get_fail_response(message)

        except Exception as e:
            message = str(e)
            return self.get_fail_response(message)
        return res

    @http.route('/attendance/check', type='json', auth='none', methods=['POST'])
    def get_emp_attendance_check(self, **kw):
        try:
            # Fetch Data Payload
            accept_language = False
            accept_language = request.httprequest.headers.get('Accept-Language')
            token = request.httprequest.headers.get('token')
            if not token or not self._is_token_valid(token):
                message = 'Invalid Token' if accept_language != 'ar' else 'رمز غير صالح'
                return self.get_fail_response(message)

            # Process the request if the token is valid
            # vals = parse_qs(request.httprequest.query_string.decode("utf-8"))
            #
            # accept_language = False
            # accept_language = request.httprequest.headers.get('Accept-Language')
            # jwt_token = request.httprequest.headers.get('jwt_token')
            # decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})
            if not kw.get('tz', False):
                message = 'Timezone(tz) is required' if accept_language != 'ar' else 'المنطقة الزمنية مطلوبه'
                return self.get_fail_response(message)

            if not kw.get('attendance_time', False):
                message = 'Attendance Time(attendance_time) is required' if accept_language != 'ar' else 'وقت الحضور مطلوب'
                return self.get_fail_response(message)

            # if "employee_id" not in decoded_token:
            #     result = {
            #         'status': False,
            #         'message': 'Invalid Token' if accept_language != 'ar' else 'رمز غير صالح'
            #     }
            #     return Response(
            #         json.dumps(result),
            #         content_type='application/json',
            #         status=401
            #     )
            employee_id = request.env['hr.employee'].sudo().search([('user_id.api_token', '=', token)])
            if not employee_id:
                message = 'Invalid Employee' if accept_language != 'ar' else 'موظف غير متوفر'
                return self.get_fail_response(message)

            attendance_env = request.env['hr.attendance'].sudo()
            employee_tz_name = request.env['hr.employee'].sudo().browse(employee_id.id).tz or 'UTC'
            try:
                payload_timezone = pytz.timezone(kw.get('tz', ""))
                employee_timezone = pytz.timezone(employee_tz_name)
            except pytz.UnknownTimeZoneError:
                message = 'Invalid Time Zone' if accept_language != 'ar' else 'منظقه زمنيه غير صالحه'
                return self.get_fail_response(message)
            attendance_time = datetime.datetime.strptime(kw.get("attendance_time", ""), '%Y-%m-%d %H:%M:%S')
            attendance_time_localized = payload_timezone.localize(attendance_time)
            attendance_time_utc = attendance_time_localized.astimezone(pytz.utc)
            attendance_time_in_employee_tz = attendance_time_utc.astimezone(employee_timezone)

            # Convert to naive datetime (remove timezone info) for storing in Odoo
            naive_attendance_time = attendance_time_in_employee_tz.replace(tzinfo=None)
            attendance_list = []

            attendance_records = attendance_env.search([('employee_id.id', '=', employee_id.id)])
            if attendance_records:
                today_records = attendance_records.filtered(lambda x: x.check_in.date() == naive_attendance_time.date())

                if today_records:
                    for record in today_records:
                        attendance_list.append({
                            "attendance_time": record.check_in.strftime('%H:%M:%S'),
                            "leave_time": record.check_out.strftime('%H:%M:%S') if record.check_out else "null",
                        })
                    res = {
                        "status": True,
                        'code': 200,
                        "message": "User Attendance" if accept_language != 'ar' else 'حضور الموظف',
                        "attendance": attendance_list
                    }
                    return res
                else:
                    message = "There is no attendance for the employee today" if accept_language != 'ar' else "لا يوجد سجل حضور للموظف اليوم"
                    return self.get_fail_response(message)
            else:
                message = "There is no attendance for the employee" if accept_language != 'ar' else "لا يوجد سجل حضور للموظف ",
                return self.get_fail_response(message)

        except Exception as e:
            # Handle exceptions
            message = str(e)
            return self.get_fail_response(message)
