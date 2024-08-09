import json
import pyproj
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TIEZone(models.Model):
    _name = 'tie.zone'

    name = fields.Char(string="name", required=True, index=True)
    latitude = fields.Float(string='Geo Latitude', digits=(16, 5), copy=False, prevent_zero=True)
    longitude = fields.Float(string='Geo Longitude', digits=(16, 5), copy=False, prevent_zero=True)
    distance = fields.Float(string="Radius")

    @api.constrains('distance')
    def _check_distance(self):
        if self.distance <= 0:
            raise models.ValidationError(_('Radius cannot be negative.'))

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if record.name and self.search_count(
                    [('name', '=', record.name), ('id', '!=', record.id)]) > 0:
                raise ValidationError('Name ID must be unique!')
