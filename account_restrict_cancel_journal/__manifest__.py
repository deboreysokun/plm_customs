# -*- coding: utf-8 -*-
{
    'name': "account_cancel_journal",
    'summary': """Restrict User to cancel the journal """,
    'description': """ Only user with Access for Cancel Journal can see the button 'Cancel' and 'Reset to draft for each invoice' """,
    'author': "A2A Digital",
    'category': 'account',
    'version': '14.0.1.0.0',
    'depends': ['account'],
    'data': [
        'views/account_cancel_journal_views.xml',
        'views/account_register_payment_views.xml',
    ],
}
