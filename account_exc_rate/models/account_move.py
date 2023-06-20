# -*- coding: utf-8 -*-
from locale import currency
from webbrowser import get
from odoo import models, fields, api,_

class account_exc_rate(models.Model):
    _inherit='account.move'
    
    ############################
    # Field & functions to computer the total amunte that from input currency khmer and thb into USD
    total_exc_khr = fields.Monetary(store=True, compute = '_compute_total_khmer', string="Total Amount in Khmer", currency_field='khr_currency_id')
    total_exc_thb = fields.Monetary(store=True, compute = '_compute_total_bat', string="Total Amount in THB", currency_field='thb_currency_id')
    rate_khr = fields.Float(string="Exchange Khmer")
    rate_thb = fields.Float(string="Exchange Thb")
    khr_currency_id = fields.Many2one('res.currency', store=True, compute = '_compute_total_khmer')
    thb_currency_id = fields.Many2one('res.currency', store=True, compute = '_compute_total_bat')

    @api.depends('amount_total')
    def _compute_total_khmer(self):
        for invoice in self:
            invoice.total_exc_khr = invoice.amount_total * invoice.rate_khr 
            invoice.khr_currency_id = self.env['res.currency'].search([('id','=',66)])

    @api.depends('amount_total')
    def _compute_total_bat(self):
        for i in self:
            i.total_exc_thb = i.amount_total * i.rate_thb
            i.thb_currency_id = self.env['res.currency'].search([('id','=',137)])
    ############################
    

    ############################
    # Field and Function inherit for Add Driver name in Accounting 
    source_origin = fields.Many2one('sale.origin', string="Source")
    approver = fields.Many2one('res.users', string="Approve By", help="សម្រាប់តែខាងផ្នែកដឹកជញ្ជូន:ត្រូវរើសអ្នកអនុញ្ញាតសម្រាប់ការស្នើរសុំបើកប្រាក់បំរុងមុន។")

    driver_names = fields.Many2many(
        comodel_name="res.partner",
        store=True,
        readonly=False,
        compute="_compute_driver_names",
        help="ឈ្មោះអ្នកបើកឡាន",
        
    )

    @api.depends("invoice_line_ids", "invoice_line_ids.move_line_ids")
    def _compute_driver_names(self):
        for invoice in self:
            invoice.driver_names = invoice.mapped(
                "invoice_line_ids.move_line_ids.picking_id.driver_name.id"
            )
    ############################


    ################################
    #function and field to get KHR currency_id and rate
    @api.returns('self')
    def _get_default_khr_exchange_currency(self): 
        return self.env['res.currency'].search([('name', '=', 'KHR')], limit=1)
    khr_exchange_currency_id = fields.Many2one('res.currency',readonly=True, tracking=True, required=True,
        states={'draft': [('readonly', False)]}, default=_get_default_khr_exchange_currency)
    
    khr_exchange_rate = fields.Float('KHR Riel Exchange Rate', store=True, readonly=True, compute="_compute_khr_exchange_rate")
    @api.depends('khr_exchange_currency_id','date')
    def _compute_khr_exchange_rate(self):
        for move in self:
            currency_rates = move.khr_exchange_currency_id._get_rates(move.company_id, move.invoice_date or fields.Date.today())
            move.khr_exchange_rate = currency_rates.get(move.khr_exchange_currency_id.id) or 1.0

    #function and field to get THB currency_id and rate
    @api.returns('self')
    def _get_default_thb_exchange_currency(self): 
        return self.env['res.currency'].search([('name', '=', 'THB')], limit=1)
    thb_exchange_currency_id = fields.Many2one('res.currency',readonly=True, tracking=True, required=True,
        states={'draft': [('readonly', False)]}, default=_get_default_thb_exchange_currency)
    
    thb_exchange_rate = fields.Float('Thai Bath Exchange Rate', store=True, readonly=True, compute="_compute_thb_exchange_rate")
    @api.depends('thb_exchange_currency_id','date')
    def _compute_thb_exchange_rate(self):
        for move in self:
            currency_rates = move.thb_exchange_currency_id._get_rates(move.company_id, move.invoice_date or fields.Date.today())
            move.thb_exchange_rate = currency_rates.get(move.thb_exchange_currency_id.id) or 1.0
    
    #############################


    ############################
    #Function to Get Payment_ids
    payment_ids = fields.Many2many(comodel_name="account.payment", store=True,compute="_get_payment_ids")
    
    @api.depends('invoice_payments_widget')
    def _get_payment_ids(self):
        for move in self:
            move.payment_ids = False
            payment_vals={}
            if move.invoice_payments_widget:
                payment_vals = move._get_reconciled_info_JSON_values()
                for payment in payment_vals:
                    move.payment_ids += self.env['account.payment'].browse(payment['account_payment_id'])
            else:
                move.payment_ids = False
                
    
    #Compute Date & Rate from Register Payment
    date_register = fields.Date('Register Date',store=True,compute="_compute_register_date")
    @api.depends('payment_ids')
    def _compute_register_date(self):
        for record in self:
            if record.payment_ids:
                for pay in record.payment_ids:        
                    record.date_register = pay.date
            else:
                record.date_register = False
    payment_ref = fields.Char('Memo/Respect Note',store=True,compute="_compute_payment_ref")
    @api.depends('payment_ids')
    def _compute_payment_ref(self):
        for record in self:
            if record.payment_ids:
                for pay in record.payment_ids:        
                    record.payment_ref = pay.ref
            else:
                record.payment_ref = False
              
    khr_rate_register = fields.Float('KHR Rate Register',store=True,compute="_compute_khr_register_rate")
    thb_rate_register = fields.Float('THB Rate Register',store=True,compute="_compute_thb_register_rate")
    @api.depends('payment_ids')
    def _compute_payment_currency(self):
        for record in self:
            payment_currency_id = record.company_currency_id.id
            if record.payment_ids:
                for rec in record.payment_ids:
                    payment_currency_id = rec.currency_id.id
        return payment_currency_id

    # @api.depends('payment_ids')
    # def _compute_register_rate(self):
    #     for rec in self:
    #         currency = rec._compute_payment_currency()
    #         currency_id = self.env['res.currency'].search([('id','=',currency)], limit=1)
    #         currency_rates = currency_id._get_rates(rec.company_id, rec.date_register or fields.Date.today())
    #         rec.rate_register = currency_rates.get(currency_id.id) or 1.0

    @api.depends('payment_ids')
    def _compute_khr_register_rate(self):
        for rec in self:
            currency = rec._compute_payment_currency()
            currency_id = self.env['res.currency'].search([('id','=',currency)], limit=1)
            khr_currency_id = currency_id.env['res.currency'].search([('name','=','KHR')], limit=1)
            currency_rates = khr_currency_id._get_rates(rec.company_id, rec.date_register or fields.Date.today())
            rec.khr_rate_register = currency_rates.get(khr_currency_id.id) or 1.0

    @api.depends('payment_ids')
    def _compute_thb_register_rate(self):
        for rec in self:
            currency = rec._compute_payment_currency()
            currency_id = self.env['res.currency'].search([('id','=',currency)], limit=1)
            thb_currency_id = currency_id.env['res.currency'].search([('name','=','THB')], limit=1)
            currency_rates = thb_currency_id._get_rates(rec.company_id, rec.date_register or fields.Date.today())
            rec.thb_rate_register = currency_rates.get(thb_currency_id.id) or 1.0
            
    @api.onchange('date_register')
    def _onchange_register_rate(self):
        self._compute_khr_register_rate
        self._compute_thb_register_rate
    ##########################


   



        