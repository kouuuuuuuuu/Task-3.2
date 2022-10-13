

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from datetime import datetime

from odoo.exceptions import ValidationError


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
    assigneeUpdateDate = fields.Datetime(string='Assignee Update At Time')
    tags = fields.Char(string='Tags')
    customer = fields.Many2one('res.partner', string='Customer')
    @api.onchange('assign_to')
    def updateTime(self):
        now = datetime.now()
        for record in self:
            if self.assign_to:
                self.assigneeUpdateDate = now
    @api.onchange('assigneeUpdateDate')
    def autoFill(self):
        if self.assigneeUpdateDate:
            self.tags = 'New feature'
    @api.constrains('customer')
    def checkCustomer(self):
        for rec in self:
            if rec.customer.id:
                check = self.env['project.study'].search([('customer', '=', rec.customer.id), ('id', '!=', rec.id)])
                if check:
                    raise ValidationError(rec.customer.name + 'is existed at another task. Please choose another customer')