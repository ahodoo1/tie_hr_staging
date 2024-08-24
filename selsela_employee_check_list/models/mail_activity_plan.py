# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class MailActivityPlan(models.Model):
    _inherit = 'mail.activity.plan'

    def unlink(self):
        """
        Function is used for checking while deleting
        plan which is related to checklist record
        and raise error.

        """
        on_id = self.env.ref('hr.onboarding_plan')
        of_id = self.env.ref('hr.offboarding_plan')
        for recd in self:
            if recd.id == of_id.id or recd.id == on_id.id:
                raise UserError(_("Checklist Record's Can't Be Delete!"))
        return super().unlink()
