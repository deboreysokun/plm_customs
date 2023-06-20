# -*- coding: utf-8 -*-

from odoo import models, fields, api

class account_exc_rate(models.Model):
    _inherit='account.move.line'

    product_line_date = fields.Date(
        string='Date',
        index=True,
    )