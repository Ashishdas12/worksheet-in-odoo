from odoo import models, fields, api, _
from odoo import http


class astask(models.Model):
    _name = 'astask.astask'
    _description = 'astask astask'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    us_name = fields.Many2one('res.users', string='UserName', default=lambda self: self.env.user.id, readonly=True)
    proj_id = fields.Many2one('project.project', string="Project")
    task_id = fields.Many2one('project.task', string="Task")
    # working or not find
    demotest = fields.Selection([
        ('working', 'Working'),
        ('onhold', 'Onhold'),
        ('done', 'Done')

    ], default='working', string='Status')
    # statusbar
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('cancel', 'Cancelled'),
        ('done', 'Done'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    @api.model
    def get_astask_data(self):
        user_records = []

        # Fetching the current user
        current_user = self.env.user

        if current_user.has_group('Digitzz.digitz_admin'):
         # Check if current user is in 'admin' group
            # Fetch all records for 'admin' users
            users = self.search([])
        elif current_user.has_group('Digitzz.digitz_employee'):
            print("hello employee")# Check if current user is in 'employee' group
            # Fetch records only for the current 'employee' user
            users = self.search([('us_name', '=', current_user.id)])
        else:

            # For other users, return an empty list or handle accordingly
            return user_records

        # Process the records as before
        for user in users:
            user_data = {
                'name': user.name,
                'us_name': user.us_name.name if user.us_name else '',
                'proj_id': user.proj_id.name if user.proj_id else '',
                'task_id': user.task_id.name if user.task_id else '',
                'demotest': user.demotest,
                'state': user.state,
            }
            user_records.append(user_data)

        return user_records



    # # og
    # @api.model
    # def get_astask_data(self):
    #
    #     user_records = []
    #
    #
    #     users = self.search([])
    #     for user in users:
    #         user_data = {
    #             'name': user.name,
    #             'us_name': user.us_name.name if user.us_name else '',
    #             'proj_id': user.proj_id.name if user.proj_id else '',
    #             'task_id': user.task_id.name if user.task_id else '',
    #             'demotest': user.demotest,
    #             'state': user.state,
    #
    #         }
    #         user_records.append(user_data)
    #
    #     return user_records





    # ochange project and task
    @api.onchange('proj_id')
    def _onchange_proj_id(self):
        if self.proj_id:
            dom = [('project_id', '=', self.proj_id.id)]
            return {'domain': {'task_id': dom}}
        else:
            return {'domain': {'task_id': []}}

    # onchange function during if any change in
    # task the automaticly related changes appear
    # on project field using on change  mutually changes using two codes
    @api.onchange('task_id')
    def _onchange_task_id(self):
        if self.task_id:
            self.proj_id = self.task_id.project_id
        else:
            self.proj_id = False


# 2ndclassmytask
class mytask(models.Model):
    _name = 'mytask.mytask'
    _description = 'mytask mytask'
