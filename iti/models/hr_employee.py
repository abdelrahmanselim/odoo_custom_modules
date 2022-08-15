from odoo import fields, models


class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    phone2 = fields.Char("Phone 2")

    # data
    # business