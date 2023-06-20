# -*- coding: utf-8 -*-
{
    'name': "account_move_line_date",
    'summary': """ Add field date in move line""",
    'description': """
        - Add Fields Date for each line in account.move.line
    """,
    'author': "Jenny Sun",
    'category': 'Extra Tool',
    'version': '14.0.1.0.0',
    'depends': ['account',],
    'data': [
        'views/account_move_line_date_views.xml'
    ],
    'demo': [],
}
