import json
import pyproj
from odoo import api, fields, models, _
from math import cos, sin, sqrt, atan2, radians
from odoo.exceptions import ValidationError, AccessError


def get_google_maps_url(latitude, longitude):
    return "https://maps.google.com?q=%s,%s" % (latitude, longitude)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    location_record = fields.Boolean(string="Location Record", readonly=True, default=False, copy=False)
    check_in_latitude = fields.Float(string='Sign-in Latitude', digits=(16, 6), readonly=True, copy=False)
    check_in_longitude = fields.Float(string='Sign-in Longitude', digits=(16, 6), copy=False, readonly=True)
    check_out_latitude = fields.Float(string='Sign-out Latitude', digits=(16, 6), copy=False, readonly=True)
    check_out_longitude = fields.Float(string='Sign-out Longitude', digits=(16, 6), copy=False, readonly=True)
    check_in_zone_id = fields.Many2one(comodel_name='tie.zone', string="Sign-in Zone",
                                       compute="compute_check_in_zone_id")
    check_out_zone_id = fields.Many2one(comodel_name='tie.zone', string="Sign-out Zone",
                                        compute="compute_check_out_zone_id")
    sign_in_status = fields.Selection([('in-zone', 'In-zone'), ('out-zone', 'Out-zone')], compute="com_sign_in_status")
    sign_out_status = fields.Selection([('in-zone', 'In-zone'), ('out-zone', 'Out-zone')],
                                       compute="com_sign_out_status")

    def generate_google_maps_url(self):
        api_key = 'AIzaSyBCmvMVdGo0jXMsFdP5_zRZabfK-2e4GxE'
        points = []
        zone_ids = self.env['tie.zone'].sudo().search([])
        for zone in zone_ids:
            points.append((zone.latitude, zone.longitude))
        base_url = "https://maps.googleapis.com/maps/api/staticmap?"
        size = "600x400"
        params = {
            "size": size,
            "maptype": "roadmap",
            "markers": [],
            "key": api_key
        }

        for point in points:
            lat, lon = point
            params["markers"].append(f"{lat},{lon}")

        markers_param = "&".join(f"markers={marker}" for marker in params["markers"])
        url = f"{base_url}size={params['size']}&{markers_param}&key={api_key}"

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'
        }

    @api.model
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
        earth_radius = 6371.0
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c
        return distance * 1000  # Convert to meters

    @api.model
    def areas_intersect(self, lat1, lon1, lat2, lon2, threshold_distance):
        # Calculate the distance between the two points
        distance = self.calculate_distance(lat1, lon1, lat2, lon2)
        # Check if the distance is less than or equal to the threshold
        return distance <= threshold_distance

    @api.depends('check_in_zone_id')
    def com_sign_in_status(self):
        for rec in self:
            sign_in_status = 'out-zone'
            if rec.check_in_zone_id:
                sign_in_status = 'in-zone'
            rec.sign_in_status = sign_in_status

    @api.depends('check_out_zone_id')
    def com_sign_out_status(self):
        for rec in self:
            sign_out_status = 'out-zone'
            if rec.check_out_zone_id:
                sign_out_status = 'in-zone'
            rec.sign_out_status = sign_out_status

    @api.depends('check_in_latitude', 'check_in_longitude')
    def compute_check_in_zone_id(self):
        zones = self.env['tie.zone'].search([])
        for rec in self:
            check_in_zone_id = False
            for zone in zones:
                zone_lat = zone.latitude
                zone_long = zone.longitude
                distance = zone.distance
                intersect = self.areas_intersect(rec.check_in_latitude, rec.check_in_longitude, zone_lat, zone_long,
                                                 distance)
                if intersect:
                    check_in_zone_id = zone.id
                    break
            rec.check_in_zone_id = check_in_zone_id

    @api.depends('check_out_latitude', 'check_out_longitude')
    def compute_check_out_zone_id(self):
        zones = self.env['tie.zone'].search([])
        for rec in self:
            check_out_zone_id = False
            for zone in zones:
                zone_lat = zone.latitude
                zone_long = zone.longitude
                distance = zone.distance
                intersect = self.areas_intersect(rec.check_out_latitude, rec.check_out_longitude, zone_lat, zone_long,
                                                 distance)
                if intersect:
                    check_out_zone_id = zone.id
                    break
            rec.check_out_zone_id = check_out_zone_id

    @api.constrains('check_in_longitude', 'check_out_longitude')
    def _check_longitude(self):
        for record in self:
            if not (-180.00 <= record.check_in_longitude < 180.00):
                raise ValidationError(_("The Check in longitude must be in [-180, 180)"))
            if not (-180.00 <= record.check_out_longitude < 180.00):
                raise ValidationError(_("The Check out longitude must be in [-180, 180)"))

    @api.constrains('check_in_latitude', 'check_out_latitude')
    def _check_latitude(self):
        for record in self:
            if not (-90.00 <= record.check_in_latitude <= 90.00):
                raise ValidationError(_("The Check in latitude must be in [-90, 90]"))
            if not (-90.00 <= record.check_out_latitude <= 90.00):
                raise ValidationError(_("The Check out latitude must be in [-90, 90]"))

    def action_in_attendance_maps(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': get_google_maps_url(self.check_in_latitude, self.check_out_longitude),
            'target': 'new'
        }

    def action_out_attendance_maps(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': get_google_maps_url(self.check_out_latitude, self.check_out_longitude),
            'target': 'new'
        }
