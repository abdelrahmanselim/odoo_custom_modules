from odoo import models,fields

class Log_Patient(models.Model):
   _name = 'log.patient'
   _rec_name = 'descreption'
   descreption = fields.Text()
   patient_id = fields.Many2one('hms.patient')