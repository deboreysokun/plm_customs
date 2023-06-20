from odoo import models, fields, api

class StockDate(models.Model):
    _inherit = 'stock.inventory'

    date = fields.Datetime(required=False)
    

    def _action_start(self):
        """ Confirms the Inventory Adjustment and generates its inventory lines
        if its state is draft and don't have already inventory lines (can happen
        with demo data or tests).
        """
        for inventory in self:
            if inventory.state != 'draft':
                continue
            vals = {
                'state': 'confirm',
                # 'date': fields.Datetime.now()
            }
            if not inventory.line_ids and not inventory.start_empty:
                self.env['stock.inventory.line'].create(inventory._get_inventory_lines_values())
            inventory.write(vals)

class StockDateLine(models.Model):
    _inherit = 'stock.inventory.line'

    inventory_date = fields.Datetime('Inventory Date')
    def action_refresh_quantity(self):
        filtered_lines = self.filtered(lambda l: l.state != 'done')
        for line in filtered_lines:
            if line.outdated:
                quants = self.env['stock.quant']._gather(line.product_id, line.location_id, lot_id=line.prod_lot_id, package_id=line.package_id, owner_id=line.partner_id, strict=True)
                if quants.exists():
                    quantity = sum(quants.mapped('quantity'))
                    if line.theoretical_qty != quantity:
                        line.theoretical_qty = quantity
                else:
                    line.theoretical_qty = 0
                line.inventory_date = fields.Datetime()