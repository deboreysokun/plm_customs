# -*- coding: utf-8 -*-
{
    'name': "warning_invoice",
    'summary': """   """,
    'description': """
        To make product that sale in different from from list price is load the color in accounting
    """,
    'author': "Jenny",
    'category': 'accounting',
    'version': '14.0.1.0.0',
    'depends': ['account'],
    'data': [
        'views/account_invoice_warning_views.xml',
    ],
    "installable": True,
}
