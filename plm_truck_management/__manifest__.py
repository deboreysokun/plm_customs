# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "PLM Truck Management",
    "summary": "Keep tracking on truck repair maintance and fuel log record",
    "version": "14.0.1.0.0",
    "category": "fleet",
    "website": "https://a2a-digital.com/",
    "author": "A2A Digital",
    "license": "AGPL-3",
    "depends": ['base', 'mail',],
    "data": [
        
        "security/truck_group_users.xml",
        "security/ir.model.access.csv",
        "views/truck_view.xml",
        "reports/report_vehicle_history.xml",
        "reports/report.xml",

    ],
    "application": False,
    "installable": True,
}
