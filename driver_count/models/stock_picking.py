# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = ['stock.picking']

    driver_name = fields.Many2one('res.partner',string="Driver Name", store=True, randomly=True,)

            