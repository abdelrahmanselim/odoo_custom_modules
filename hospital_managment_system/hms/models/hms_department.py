from odoo import models,fields
class Department(models.Model):
    _name = 'hms.department'
    name=fields.Char(string="Name")
    capicty=fields.Integer()
    is_opend=fields.Boolean()
    patient_id=fields.One2many('hms.patient','dep_id')