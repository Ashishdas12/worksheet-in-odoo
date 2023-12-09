from odoo import models, fields


class Digitzz(models.Model):
    _name = 'mod.mod'
    _description = 'mod mod'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    demoo = fields.Char(string="Customername")
