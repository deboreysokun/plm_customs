# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_journal(models.Model):
    _inherit='sale.order'
    
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        domain=[("type", "=", "sale")],
    )