from odoo.exceptions import ValidationError
from odoo import models, fields, api
from odoo.exceptions import UserError

class Pateint(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'
    first_name = fields.Char(string="First Name" ,required=True)
    second_name = fields.Char(string="Second Name",required=True)
    email = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    age = fields.Integer(compute="calc_Age",store=True)
    cr_ratio = fields.Float(string="CR Ratio")
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    blood_typ = fields.Selection(
        [("a", "A"),
         ("b", "B"),
         ("o+", "O+"),
         ("a-", "A-")]
    )
    dep_id=fields.Many2one('hms.department')
    department_capicity=fields.Integer(related='dep_id.capicty', store=False)
    doctor_ids=fields.One2many('doctors.patient.line','patient_id')
    pateint_hsitory=fields.One2many('log.patient','patient_id')
    #customer_ids=fields.One2many('res.partner','related_patient_id')
    state = fields.Selection(
        [("undetermined", "Undetermined"),
         ("good", "Good"),
         ("fair", "Fair"),
         ("serious", "Serious")]
    )
    def action_undetermined(self):
        self.state = 'undetermined'
        self.env['log.patient'].create({"descreption": "state is Undetermined", "patient_id": self.id})
    def action_good(self):
        self.state = 'good'
        self.env['log.patient'].create({"descreption": "state is Good", "patient_id": self.id})
    def action_fair(self):
        self.state = 'fair'
        self.env['log.patient'].create({"descreption": "state is Fair", "patient_id": self.id})
    def action_serious(self):
        self.state = 'serious'
        self.env['log.patient'].create({"descreption": "state is Serious", "patient_id": self.id})

    @api.model
    def create(self, vals):
        email = vals['email']
        if email:
            if '@' and '.' in email:
                search_email = self.search([('email', '=', vals['email'])])
                if search_email:
                    raise UserError("email is exist")
                return super().create(vals)
            raise UserError("email not valid")

    def write(self, vals):
        email = vals['email']
        if email:
            if '@' and '.' in email:
                search_email = self.search([('email', '=', vals['email'])])
                if search_email:
                    raise UserError("email is exist")
                super().write(vals)
            else:
                raise UserError("email not valid")
        else:
            raise UserError("please type email")
    @api.depends("birth_date")
    def calc_Age(self):
        for patient in self:
            if patient.birth_date:
                today = fields.Date.today()
                print("today",today)
                delta = (today-patient.birth_date).days
                print("delta",delta)
                patient.age = delta // 365
            else:
                patient.age = 0
    @api.onchange('age')
    def change_pcr(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Age Lower than 30 ',
                    'message': 'pcr is checked Age Lower than 30'
                }
            }


