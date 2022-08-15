from odoo import fields,api,models
from odoo.exceptions import UserError


class Customer_hms(models.Model):
    _inherit = 'res.partner'
    related_patient_id = fields.Many2one('hms.patient')

    def unlink(self):
        if not self.related_patient_id:
                 super().unlink()
        else:
            raise UserError("NOT ACCESS TO DELETE CUSTOMER ")

