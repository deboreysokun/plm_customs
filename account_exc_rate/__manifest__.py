# -*- coding: utf-8 -*-
{
    'name': "account_move_inherit",
    'summary': """ Add 2 fields more for exchange rate in khmer and thai bath """,
    'description': """
        - Exchange Rate in KHR and THB 
        - Display driver name from picking in invoice
        - Display Exchange rate based on Invoice Date
        - Inherit Payment_id to display Date and Rate based on Payment date 
    """,
    'author': "A2A Digital , Jenny Sun ",
    'category': 'PLM',
    'version': '14.0.1.0.0',
    'depends': ['account','stock_picking_invoice_link'],
    'data': [
        'views/account_move_inherit_views.xml',
    ],
    'demo': [],
}
