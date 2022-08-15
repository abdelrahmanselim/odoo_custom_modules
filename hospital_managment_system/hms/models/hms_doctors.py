from odoo import models,fields
class Doctor(models.Model):
    _name = 'hms.doctors'
    _rec_name = 'first_name'
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    image = fields.Image()
    patient_id=fields.One2many('doctors.patient.line','doctor_id')

class DOCTORS_AND_PATIENT(models.Model):
    _name = 'doctors.patient.line'
    doctor_id =fields.Many2one('hms.doctors')
    patient_id=fields.Many2one('hms.patient')