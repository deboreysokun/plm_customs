from odoo import api, fields, models

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    vendor_name_id = fields.Many2one('account.move',)
    print("+++++++++", vendor_name_id)
    # vendor_name = fields.Char('Vendor Name', store=True,compute="get_default_vendor_name")
    # @api.depends('vendor_bill_id')
    # def get_default_vendor_name(self):
    #     for i in self.env.vendor_name_id:
    #         if i.vendor_bill_id:
    #             for n in i.vendor_bill_id:
    #                 i.vendor_name = n.partner_id
    #             else:
    #                 i.vendor_name = ""
    # print ("++++++++", vendor_name)

    