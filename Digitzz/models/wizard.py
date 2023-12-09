from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
import pytz
from datetime import datetime


class Wizard(models.Model):
    _name = 'wiz.wiz'
    _description = 'wiz wiz'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    date = fields.Date(required=True, default=fields.Date.context_today, readonly=True)
    datee = fields.Date(required=True, default=fields.Date.context_today, readonly=True)

    user_id = fields.Many2one('res.users', string='UserName', default=lambda self: self.env.user.id, readonly=True)

    odmsr_ids = fields.One2many('task.connect', 'linking_id', string="df")

    current_time = fields.Char(string='Time', compute='_compute_current_time')

    # s2this is used for button dissappear function
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], default='draft', string='state', readonly=True, copy=False)

    # chptD90 for systray on c
    # lick the icon in dropdwon working test
    # steop1


    @api.model
    def get_worksheet_data(self):
        data = []

        # Check if the current user belongs to the 'admin' group
        if self.env.user.has_group('Digitzz.digitz_admin'):
            users = self.env['res.users'].search([])
        # Check if the current user belongs to the 'Employee' group
        elif self.env.user.has_group('Digitzz.digitz_employee'):
            # Show data for the current user only
            users = self.env['res.users'].search([('id', '=', self.env.user.id)])
        else:
            # Default behavior if user doesn't belong to any defined group
            return data

        for x in users:
            worksheets = self.search([('user_id', '=', x.id), ('date', '=', fields.Date.today())])
            user_data = []
            for y in worksheets:
                proj_data = []
                for n in y.odmsr_ids:
                    proj_data.append({
                        'name': n.name,
                        'current_time': n.current_time,
                        'proj_id': n.proj_id.name,
                        'task_id': n.task_id.name,
                        'demotest': n.demotest,
                    })
                user_data.append({
                    'user_id': y.user_id.name,
                    'date': y.date,
                    'odmsr_ids': proj_data,
                })
            data.append({
                'user_name': x.name,
                'worksheet_data': user_data,
            })

        return data




    #  1 using Serveraction updates record into popuplike wizard  window alreedy updated
    # record are shown in the line by line like view use this code
    @api.model
    def work(self):
        # d8 create a user its used to show current user name in log in
        user = self.env.user
        today = fields.Date.context_today(self)
        current_record = self.search([('date', '=', today), ('user_id', '=', user.id)], limit=1)
        if current_record:

            return {
                'name': 'DIGITZ',
                'type': 'ir.actions.act_window',
                'res_model': 'wiz.wiz',
                'view_mode': 'form',
                'res_id': current_record.id,
                'target': 'current',
            }
        else:
            return {
                'name': 'DIGITZ',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'wiz.wiz',
                'target': 'current',
            }

    # chtgpt disppear buttonlatescode and add datas in to timesheet
    #  2   this code is add datas into timesheet
    #       account.analy is timesheetmodel id..

    def print_timesheet(self):
        today = fields.Date.context_today(self)
        existing_record = self.env['account.analytic.line']

        if existing_record:
            raise UserError("An entry for today already exists. You can't add another entry for the same day.")
        else:
            for i in self.odmsr_ids:
                if not i.proj_id or not i.task_id or not i.name or not i.current_time:
                    raise UserError("Please fill in all fields to create a timesheet entry.")
            for i in self.odmsr_ids:
                val = self.env['account.analytic.line'].create({
                    'date': today,
                    'project_id': i.proj_id.id,
                    'task_id': i.task_id.id,
                    'name': i.name,
                    'unit_amount': i.current_time,
                    'user_id': self.env.user.id,
                })
                self.state = 'done'
                return val


# 2nd class task
class Tasks(models.Model):
    _name = 'task.connect'

    linking_id = fields.Many2one("wiz.wiz")

    name = fields.Char(string="Name")
    proj_id = fields.Many2one('project.project', string="Project")
    task_id = fields.Many2one('project.task', string="Task")
    # T2
    current_time = fields.Float(string='Time')

    # CPT current user name show in the wizarlike  form defult automatic view is read only
    usname = fields.Many2one('res.users', string='UserName', default=lambda self: self.env.user.id, readonly=True)

    # newicon pause play field

    demotest = fields.Selection([
        ('working', 'Working'),
        ('onhold', 'Onhold'),
        ('done', 'Done')

    ], default='working', string='Status')

    # 98758686 check table colr change not workperson find task

    # only one user can add at atime record

    # T2Compute the current time as a float
    # def _compute_current_time(self):
    #     for record in self:
    #         gmt_time = datetime.now(pytz.timezone('Etc/GMT-0'))
    #         ist_timezone = pytz.timezone('Asia/Kolkata')
    #         ist_time = gmt_time.astimezone(ist_timezone)
    #
    #         # Format the time in 24-hour format (hh:mm)
    #         time_24_hour = ist_time.strftime('%H.%M')
    #         record.current_time = time_24_hour

    # 3
    # onchange function during if any change in
    # project the automaticly related changes appear
    # on task field using on change

    # onchange function during if any change in
    # task the automaticly related changes appear
    # on project field using on change  mutually changes using two codes
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
# this is final
