from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api


class ItiStudent(models.Model):
    _name = 'iti.student'  # part1.part2, student.student -> student_student, iti.student -> iti_student
    _rec_name = 'first_name'

    first_name = fields.Char(size=20, string='Student First Name', required=False)  # First Name
    second_name = fields.Char()
    birth_date = fields.Date()
    age = fields.Integer(compute="_get_age", store=True)
    address = fields.Char()
    phone = fields.Char()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ])

    history = fields.Text()
    cv = fields.Html()
    image = fields.Image()  # Image, Binary
    state = fields.Selection([
        ('first_interview', 'First Interview'),
        ('second_interview', 'Second Interview'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='first_interview')

    salary = fields.Float(default=100)
    tax = fields.Float()
    email = fields.Char(string="Student Email")
    accepted = fields.Boolean()

    track_id = fields.Many2one('iti.track')
    track_capacity = fields.Integer(related="track_id.capacity", store=False)
    track_name = fields.Char(related='track_id.name', readonly=False, store=True)

    skill_ids = fields.Many2many('student.skills')

    """
    Many2many 
    
    Pivote Table  iti_student_student_skills_rel 
    
    Two Columns :
            1- iti_student_id 
            2- student_skills_id
    
    
    """

    """
    Selection is list of tuples 
    First Interview ,
    Second Interview,
    Accepted 
    Rejected
    
    """

    """
    Modifiers  
        1- readonly 
        2- required
        3- invisible 
        
    """

    @api.onchange('track_id', 'accepted')
    def change_salary(self):
        # print('self ', self)
        # print('track ', self.track_id, self.track_id.name)
        # print('accepted', self.accepted)
        domain = []
        # business logic
        if self.track_id and self.accepted:
            # domain = ['|', ('is_open', '=', True), ('is_open', '=', False)]
            self.salary = 1000
            return {
                'domain': {'track_id': domain},
                'warning': {
                    'title': 'Student Accepted',
                    'message': 'Student is Accepted and change salary to 1000'
                }
            }
        else:
            print('On Change')
            # self.salary = 0

    def action_second_interview(self):
        if self.track_id:
            self.state = 'second_interview'
        else:
            raise ValidationError('Must be track on student')

    def action_accepted(self):
        self.state = 'accepted'

    def action_rejected(self):
        self.state = 'rejected'

    def action_first_interview(self):
        self.state = 'first_interview'

    @api.model
    def create(self, vals):
        # print("self ", self)
        # print("Vals ", vals)
        # business logic
        # get first name
        # get first character of second name
        # concat between , first_name.s@mycompany.com
        # update email with new value
        # if vals.get('first_name') and vals.get('second_name'):
        #     email = f'{vals.get("first_name")}.{vals.get("second_name")[0]}@mycompany.com'
        #     vals['email'] = email
        student = super().create(vals)
        # business logic
        # print("Student ", student)
        # print("Student Fisrt Name ", student.first_name)
        # print("Student Second Name ", student.second_name)
        if student.first_name and student.second_name:
            email = f'{student.first_name}.{student.second_name[0]}@mycompany.com'
            student.email = email
        return student

    def write(self, vals):
        # print("Vals ", vals)
        # print("self ", self)
        # print('first_name ', self.first_name)
        # logic
        # if vals.get('first_name') or vals.get('second_name'):
        #     if vals.get('first_name'):
        #         email = f'{vals.get("first_name")}'
        #     else:
        #         email = f'{self.first_name}'
        #     if vals.get('second_name'):
        #         email += f'.{vals.get("second_name")[0]}@mycompany.com'
        #     else:
        #         email += f'.{self.second_name[0]}@mycompany.com'
        #
        #     vals['email'] = email  # vals.update({'email': email})
        #     print('vals ', vals)
        res = super().write(vals)
        # logic
        if vals.get('first_name'):
            email = f'{vals.get("first_name")}'
        else:
            email = f'{self.first_name}'
        if vals.get('second_name'):
            email += f'.{vals.get("second_name")[0]}@mycompany.com'
        else:
            email += f'.{self.second_name[0]}@mycompany.com'
        if vals.get('first_name') or vals.get('second_name'):
            # print("Email ", email)
            # print("Self Email ", self.email)
            self.email = email  # call write again , vals {'email': email}

        # track = self.env['iti.track'].browse(1) # iti.track(1,) , iti.track()
        # track = self.env['iti.track'].browse([1, 4]) # iti.track(1,4) , iti.track()

        return res

    def unlink(self):
        print("record ", self)
        for student in self:
            if student.track_id:
                raise UserError(f"Not Allowed deleting student linked with track {student.track_id.name}")
        return super().unlink()

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'This email exists')
    ]

    # business as constraints
    # @api.constrains('track_id')
    # def check_track_capacity(self):
    #     if self.track_id:
    #         # print("self ", self)
    #         # print("self.track ", self.track_id, "track_capacity ", self.track_id.capacity)  # iti.track(id, )
    #         # print("student on track ", self.track_id.student_ids)
    #         track = self.track_id
    #         # student_on_track = self.track_id.student_ids
    #         student_on_track = self.search([('track_id', '=', track.id)])
    #         # print('track', track)
    #         # print('student on track ', student_on_track)
    #         if len(student_on_track) > track.capacity:
    #             raise UserError('Track is full completely')

    # compute fucntion
    @api.depends('birth_date')
    def _get_age(self):
        print("records  ", self)
        for student in self:
            if student.birth_date:
                today = fields.Date.today()
                delta = (today - student.birth_date).days
                student.age = delta // 365
            else:
                student.age = 0


class StudentSkills(models.Model):
    _name = 'student.skills'

    name = fields.Char()
    level = fields.Selection([
        ('good', 'Good'),
        ('very_good', 'Very Good'),
    ])
