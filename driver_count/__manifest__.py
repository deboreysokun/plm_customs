# -*- coding: utf-8 -*-
{
    'name': "driver_count",
    'summary': """ To add driver name for each picking stocks """,
    'description': """ Warehouse manager can select one of the driver for the sale order and Accountant also can see which car has been drive by who how many time """,
    'author': "Jenny",
    'category': 'inventory',
    'version': '14.0.1.0.0',
    'depends': ['stock'],
    'data': [
        'views/driver_name_views.xml',
        ],
    'demo': [],
    "installable": True,
    "license": "AGPL-3",
}
