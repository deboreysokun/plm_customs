# -*- coding: utf-8 -*-
{
    'name': "PLM Template Payment",
    'summary': """ PLM Templates Payment""",
    'description': """
        PLM Templates Report for 
        - Statement Expense
    """,
    'author': "Jenny Sun ",
    'category': 'PLM',
    'version': '14.0.1.0.0',
    'depends': ['base','account'],
    'data': [
        'views/web.xml',
        'reports/report_statement_expense.xml',
    ],
    'demo': [],
    'installable': True,
}