from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'account.move.line'

    plate_num = fields.Many2one(
        'res.partner', 
        string="Plate Number",
        help="ផ្លាកលេខឡាន",
    )
    inv_ref = fields.Char(string="Invoice Reference",)




