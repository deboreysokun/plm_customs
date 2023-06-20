# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import string
from odoo import api, fields, models, _


class Truck(models.Model):
    _name = 'truck.truck'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Truck'


    name = fields.Char(store=True, required=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    register_number = fields.Char(tracking=True, string='Register No.')
    buy_date = fields.Date(string="Buy Date")
    license_plate = fields.Char(tracking=True, string='Plate No.',
        help='License plate number of the Truck')
    chassis = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)', copy=False)
    driver_ids = fields.Many2many('res.partner',copy=False)
    model_id = fields.Many2one('truck.model', 'Model Name',
    tracking=True, help='Model of the Truck')
    insurance = fields.Char()
    company = fields.Char()
    expiry_date = fields.Date(string="Expiry Date", tracking=True,copy=False)
    inspection_date = fields.Date(string="Inspection Date", tracking=True,copy=False)

    maintenance_ids = fields.One2many(
        comodel_name="truck.maintenance.line",
        inverse_name="truck_id",
        string="Repair History",
        copy=False,
    )
    fuel_log_ids = fields.One2many(
        comodel_name="truck.fuel.line",
        inverse_name="truck_id",
        string="Fuel History",
        copy=False,
    )

    truck_type = fields.Selection(selection =[
                        ('diesel', 'Diesel - ប្រេងម៉ាស៊ូត'),
                        ('gas', 'Gas-ហ្គាស'),
                        ('Gasoline', 'Gasoline-សាំង')],
                        string='Type of Fuel', tracking=True)

class TruckModel(models.Model):
    _name = 'truck.model'

    name = fields.Char(stirng="Model Name", store=True)

class TruckMaintenanceLine(models.Model):
    _name = 'truck.maintenance.line'

    truck_id = fields.Many2one('truck.truck', string='Truck')
    date = fields.Date(string="Date", required=True)
    description = fields.Char(string='Description', required=True)
    amount = fields.Float(string='Cost')
    active = fields.Boolean('Active', default=True, tracking=True, compute="inactive_line")

    @api.depends('truck_id.active')
    def inactive_line(self):
        for vehicle in self:
            vehicle.active = vehicle.truck_id.active

class TruckFuelLine(models.Model):
    _name = 'truck.fuel.line'

    truck_id = fields.Many2one('truck.truck', string="Truck")
    date = fields.Date(string="Date", required=True)
    description = fields.Char('Description', required=True)
    fuel_qty = fields.Float(string='Fuel(L)')
    km = fields.Float(string="Km")
    travel_count = fields.Integer(string="Count")
    active = fields.Boolean('Active', default=True, tracking=True, compute="inactive_line")

    driver_id = fields.Many2one('res.partner', string="Driver")
    ass_driver_id = fields.Many2one('res.partner', string="Ass/Driver")

    fuel_cost = fields.Float(string="Cost of Fuel")
    commission = fields.Float(string="Commission Driver")
    revenue  = fields.Float(string="Revenue")
    legal = fields.Float(string="Legal Fee")
    gross_pro = fields.Float(string="Gross Profit", compute='_compute_gross_profit')

    customer = fields.Many2one('res.partner', string="Customer")
    

    @api.depends('truck_id.active')
    def inactive_line(self):
        for vehicle in self:
            vehicle.active = vehicle.truck_id.active

    @api.depends('fuel_cost','commission','revenue','legal')
    def _compute_gross_profit(self):
        for gf in self:
            gf.gross_pro = gf.revenue - (gf.fuel_cost + gf.commission +gf.legal)
