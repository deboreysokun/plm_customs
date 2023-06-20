

from attr import field
from odoo import models, fields, api,_

class AccountMoveLine(models.Model):
    _inherit = "account.invoice.report"

    label_name = fields.Char(string="Label Name")
    sub_pricetotal = fields.Float(string="Total Amount with Tax")
    price_unit_cus = fields.Float(string="Price Unit")
    currency_id_name = fields.Many2one('res.currency',string="Currency Type")
    amount_in_currency = fields.Monetary(currency_field="currency_id_name",string="Amount in Currency")
    move_currency_id = fields.Many2one('res.currency',string="Currency Move Type")
    rate_khr_inh = fields.Float(string="Rate KHR")
    rate_thb_inh = fields.Float(string="Rate THB")
    driver = fields.Many2one('res.partner',"Driver Name")
    register_date = fields.Date(string="Register Date")
    khr_register_rate = fields.Float(string="KHR Register Rate")
    thb_register_rate = fields.Float(string="THB Register Rate")
    inv_date = fields.Date(string="Inv or Bill Date")
    payment_refs = fields.Char(string="Memo/Respect Note")
    
    def _select(self):
        return super()._select() + " , move.payment_ref as payment_refs , move.invoice_date as inv_date , move.khr_rate_register as khr_register_rate , move.thb_rate_register as thb_register_rate , move.date_register as register_date , move.driver_names as driver , move.rate_khr as rate_khr_inh , move.rate_thb as rate_thb_inh , line.amount_currency as amount_in_currency, move.currency_id as move_currency_id, line.name as label_name , line.price_total as sub_pricetotal , line.price_unit as price_unit_cus , line.currency_id as currency_id_name"