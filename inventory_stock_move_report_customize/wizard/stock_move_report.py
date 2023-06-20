from odoo import api, fields, models
from datetime import datetime
import xlwt
from xlsxwriter.workbook import Workbook
from six import BytesIO
import base64

from werkzeug.routing import ValidationError

 
class StockMoveReport(models.TransientModel):
    """
    This model is for calculate the stock in, stock out, opening quantity and ending quantity of products in a
    specific location between a start date and an end date.
    ***Note:
    - Dummy fields are fields that need to set their Index property to False in order for the model to work due to
    the configuration from the parent model
    """

    _name = "stock.move.report"

    # Start Dummy Field
    name = fields.Char("Dummy field", default=123)
    product_id = fields.Many2one(
        'product.product', 'Product', index=False, required=False)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=False)
    move_dest_ids = fields.Integer("Dummy field")
    move_orig_ids = fields.Integer("Dummy field")
    route_ids = fields.Integer("Dummy field")
    location_id = fields.Many2one(
        'stock.location', 'Source Location', index=False, required=False)
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location', index=False, required=False)

    # End Dummy Field

    stock_move_report_excel_file = fields.Binary('Stock Move Report')
    inventory_start_date = fields.Datetime("Inventory start at Date", required=True)
    inventory_end_date = fields.Datetime("Inventory end at Date", required=True)
    location = fields.Many2one(
        'stock.location', 'Location',
        index=False, required=True,
        help="Set a location to get the product report from")

    @api.constrains('inventory_end_date', 'inventory_start_date')
    def _check_date_domain(self):
        if self.inventory_end_date >= datetime.today():
            raise ValidationError('End date must not be greater than today!')
        if self.inventory_start_date >= datetime.today():
            raise ValidationError('Start date must not be greater than today!')
        if self.inventory_start_date > self.inventory_end_date:
            raise ValidationError('Start date can not be greater than end date!')

    def get_stock_report(self):
        """
        This function is dedicated to calculate the stock report for a specific location between a start date
             and end date using a certain formula. The required data is the stock in number, the stock out number, the
             opening quantity number and ending quantity number. The formula use the current quantity of a specific
             product and the stock move of that specific products from a start date to get the opening quantity of that
             product in the specified start date.
             ***Formula -- Note that -> ( from start date to end date) = *
             - Opening quantity* = current quantity + current stock out - current stock in
             - Ending quantity*  = Opening quantity* + stock in* - stock out*
             :return: a list containing objects which has details of each item
        """
        stock_move_earliest = self.env['stock.move'].search([('create_date', '<=', datetime.today())])
        stock_move_current = self.env['stock.move'].search([('create_date', '>=', self.inventory_start_date),
                                                            ('create_date', '<=', datetime.today())])
        stock_move = self.env['stock.move'].search([('create_date', '>=', self.inventory_start_date),
                                                    ('create_date', '<=', self.inventory_end_date)])
        stock_quan = self.env['stock.quant'].search([('location_id.complete_name', '=', self.location.complete_name)])
        product_quan = {}
        
        for rec in stock_quan:
            product_quan[rec.product_id] = {
                "ref": rec.product_id.default_code,
                "name": rec.product_id.name,
                "row_num": 10,
                "opening_qty": 0,
                "ending_qty": 0,
                "stock_in": 0,
                "stock_out": 0,
                "current_quantity": rec.quantity,
                "stock_in_current": 0,
                "stock_out_current": 0
            }

        for rec in stock_move_current:
            if self.location.complete_name == rec.location_id.complete_name:
                if rec.product_id in product_quan:
                    product_quan[rec.product_id]["stock_out_current"] += rec.product_qty
                else:
                    product_quan[rec.product_id] = {
                        "ref": rec.product_id.default_code,
                        "name": rec.product_id.name,
                        "row_num": 10,
                        "opening_qty": 0,
                        "ending_qty": 0,
                        "stock_in": 0,
                        "stock_out": 0,
                        "current_quantity": 0,
                        "stock_in_current": 0,
                        "stock_out_current": 0
                    }
                    product_quan[rec.product_id]["stock_out_current"] += rec.product_qty

            elif self.location.complete_name == rec.location_dest_id.complete_name:
                if rec.product_id in product_quan:
                    product_quan[rec.product_id]["stock_in_current"] += rec.product_qty
                else:
                    product_quan[rec.product_id] = {
                        "ref": rec.product_id.default_code,
                        "name": rec.product_id.name,
                        "row_num": 10,
                        "opening_qty": 0,
                        "ending_qty": 0,
                        "stock_in": 0,
                        "stock_out": 0,
                        "current_quantity": 0,
                        "stock_in_current": 0,
                        "stock_out_current": 0
                    }
                    product_quan[rec.product_id]["stock_in_current"] += rec.product_qty

        for rec in stock_move:
            if self.location.complete_name == rec.location_id.complete_name:
                if rec.product_id in product_quan:
                    product_quan[rec.product_id]["stock_out"] += rec.product_qty
                else:
                    product_quan[rec.product_id] = {
                        "ref": rec.product_id.default_code,
                        "name": rec.product_id.name,
                        "row_num": 10,
                        "opening_qty": 0,
                        "ending_qty": 0,
                        "stock_in": 0,
                        "stock_out": 0,
                        "current_quantity": 0,
                        "stock_in_current": 0,
                        "stock_out_current": 0
                    }
                    product_quan[rec.product_id]["stock_out"] += rec.product_qty

            elif self.location.complete_name == rec.location_dest_id.complete_name:
                if rec.product_id in product_quan:
                    product_quan[rec.product_id]["stock_in"] += rec.product_qty
                else:
                    product_quan[rec.product_id] = {
                        "ref": rec.product_id.default_code,
                        "name": rec.product_id.name,
                        "row_num": 10,
                        "opening_qty": 0,
                        "ending_qty": 0,
                        "stock_in": 0,
                        "stock_out": 0,
                        "current_quantity": 0,
                        "stock_in_current": 0,
                        "stock_out_current": 0
                    }
                    product_quan[rec.product_id]["stock_in"] += rec.product_qty

        for rec in stock_move_earliest:
            if self.location.complete_name == rec.location_id.complete_name or\
                    self.location.complete_name == rec.location_dest_id.complete_name:
                if rec.product_id not in product_quan:
                    product_quan[rec.product_id] = {
                        "ref": rec.product_id.default_code,
                        "name": rec.product_id.name,
                        "row_num": 10,
                        "opening_qty": 0,
                        "ending_qty": 0,
                        "stock_in": 0,
                        "stock_out": 0,
                        "current_quantity": 0,
                        "stock_in_current": 0,
                        "stock_out_current": 0
                    }
        vals = []
        i = 1
        for product in product_quan:
            product_quan[product]["opening_qty"] = product_quan[product]["current_quantity"] \
                                                   + product_quan[product]["stock_out_current"] \
                                                   - product_quan[product]["stock_in_current"]
            product_quan[product]["ending_qty"] = product_quan[product]["opening_qty"] \
                                                  + product_quan[product]["stock_in"] \
                                                  - product_quan[product]["stock_out"]
            product_quan[product]["row_num"] = i
            i += 1
            vals.append(product_quan[product])

        for obj in vals:
            if str(obj['ref']) == "False":
                obj['ref'] = " "

        data = {
            'ids': self.ids,
            'models': self._name,
            'date_start': self.inventory_start_date,
            'date_end': self.inventory_end_date,
            'location': self.location.complete_name,
            'vals': vals
        }
        return data

    def generate_excel_report(self):
        """
        This function will generate an excel report when the user click confirm.
        The excel is created using xlwt module.
        :return: a url that leads to the download of the excel file
        """
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet('Sheet 1')
        title_style = xlwt.easyxf(
                   'font:height 500,bold True;pattern: pattern solid, fore_colour white;align: horiz center;'
                   ' borders: top_color black, bottom_color black, right_color black, left_color black,\
                   left thin, right thin, top thin, bottom thin;'
                   )
        worksheet.write_merge(1, 3, 1, 15, 'Report Inventory', title_style)
        header_style = xlwt.easyxf(
                   'font:height 250,bold True;pattern: pattern solid, fore_colour white;align: horiz center;'
                   ' borders: top_color black, bottom_color black, right_color black, left_color black,\
                   left thin, right thin, top thin, bottom thin;'
                   )
        body_style = xlwt.easyxf(
                   'font:height 250;pattern: pattern solid, fore_colour white;align: horiz center;'
                   ' borders: top_color black, bottom_color black, right_color black, left_color black,\
                   left thin, right thin, top thin, bottom thin;'
                   )
        worksheet.write_merge(5, 6, 1, 1, 'No', header_style)
        worksheet.write_merge(5, 6, 2, 3, 'Code', header_style)
        worksheet.write_merge(5, 6, 4, 7, 'Product Name', header_style)
        worksheet.write_merge(5, 6, 8, 10, 'Opening Quantity', header_style)
        worksheet.write_merge(5, 6, 11, 11, 'In', header_style)
        worksheet.write_merge(5, 6, 12, 12, 'Out', header_style)
        worksheet.write_merge(5, 6, 13, 15, 'Ending Quantity', header_style)

        top_row = 7
        bot_row = 8
        data = self.get_stock_report()['vals']
        for item in data:
            worksheet.write_merge(top_row, bot_row, 1, 1, item['row_num'], body_style)
            worksheet.write_merge(top_row, bot_row, 2, 3,  item['ref'], body_style)
            worksheet.write_merge(top_row, bot_row, 4, 7, item['name'], body_style)
            worksheet.write_merge(top_row, bot_row, 8, 10, item['opening_qty'], body_style)
            worksheet.write_merge(top_row, bot_row, 11, 11, item['stock_in'], body_style)
            worksheet.write_merge(top_row, bot_row, 12, 12, item['stock_out'], body_style)
            worksheet.write_merge(top_row, bot_row, 13, 15, item['ending_qty'], body_style)
            top_row = bot_row + 1
            bot_row += 2

        fp = BytesIO()
        workbook.save(fp)
        self.stock_move_report_excel_file = base64.encodebytes(fp.getvalue())
        fp.close()

        return {
            'type': 'ir.actions.act_url',
            'name': 'Stock move report',
            'url': '/web/content/stock.move.report/%s/stock_move_report_excel_file/stock_move_report_excel_file.xls?download=true' % (self.id),
        }

