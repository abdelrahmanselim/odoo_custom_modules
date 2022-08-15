from odoo import models, fields


class ItiCourses(models.Model):
    _name = 'iti.course'

    name = fields.Char()
    is_open = fields.Boolean()
    track_ids = fields.One2many('track.course.line', 'course_id')


class TrackCourseLine(models.Model):
    _name = 'track.course.line'

    course_id = fields.Many2one('iti.course')
    track_id = fields.Many2one('iti.track')
    hours = fields.Integer()


