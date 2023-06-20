# -*- coding: utf-8 -*-

from odoo import models, fields, api


class khmer_name(models.Model):
    _inherit = 'res.partner'

    kh_name = fields.Char(string="Khmer Name")
