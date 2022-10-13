from odoo import api, fields, models, tools, SUPERUSER_ID, _

class ProjectStudy2(models.Model):
    _inherit = 'res.users'

    project_study_id = fields.Many2one('project.study')


class ProjectStudy(models.Model):
    _name = 'project.study'

    name = fields.Char(required=True)
    dateline = fields.Date(string="DateLine", required=True)
    assign_to = fields.Many2one('res.users', string='Assigned To', default=lambda self: self.env.user)
    note = fields.Text(string='Note')
    description = fields.Html(string='Description')
    list = [
        ('TODO', 'TODO'),
        ('IN - PROGRESS', 'IN - PROGRESS'),
        ('REVIEW', 'REVIEW'),
        ('REVIEW', 'DONE')
    ]
    status = fields.Selection(selection=list, string='Status', default='TODO')
    project_managers = fields.Many2many('res.users', "user_working_rel_many2many", string='Project Managers')
    task_attendees_ids = fields.One2many('res.users', 'project_study_id', string='Task Attendees')


