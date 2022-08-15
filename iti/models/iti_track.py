from odoo import models, fields


class ItiTrack(models.Model):
    _name = 'iti.track'  # iti_track
    # _rec_name = ''

    name = fields.Char()
    address = fields.Char()
    capacity = fields.Integer(string='Number of Students')
    is_open = fields.Boolean()
    duration = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()

    student_ids = fields.One2many('iti.student', 'track_id')

    course_ids = fields.One2many('track.course.line', 'track_id')

    """
    select s.first_name, s.second_name from iti_track t, iti_student s
        where t.id = s.track_id 
        and t.id = id;
    """

