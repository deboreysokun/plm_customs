# See LICENSE file for full copyright and licensing details.
{
    "name": "Inventory Stock Move Report Customize",
    "version": "14.1.2",
    "author": "Phalla Borormey(8A)",
    "category": "Inventory",
    "summary": "Add custom Stock Move Report function, Module needed: xlwt and XlsxWriter(pip install xlwt and pip install XlsxWriter), REQ Agreement Page: 8,9",
    'depends': ['base','stock', 'product', 'uom',],
    "data": [
        'security/ir.model.access.csv',
        'wizard/stock_move_report_wizard.xml',
        'views/stock_move_report_view.xml',
    ],
    "installable": True,
}