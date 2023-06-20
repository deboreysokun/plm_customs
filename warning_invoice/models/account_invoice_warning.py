# -*- coding: utf-8 -*-

from odoo import models, fields, api


class wanring_invoice(models.Model):
    _inherit = 'account.move.line'

    price_below_cost = fields.Boolean(compute='_price_unit', readonly=True, string='Price below Cost')

    @api.depends('price_unit')
    def _price_unit(self):
        for record in self:
            record['price_below_cost'] = (record.price_unit < record.product_id.lst_price) | (record.price_unit > record.product_id.lst_price)
        
