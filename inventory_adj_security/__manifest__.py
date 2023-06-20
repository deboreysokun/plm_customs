# -*- coding: utf-8 -*-
{
    'name': "inventory_adjustment_specific_user",
    'summary': """Restrict User to for Inventory Adjustment""",
    'description': """ Only user with Access for Inventory Adjustment can see the menuitem to do Adjustment in inventory""",
    'author': "A2A Digital",
    'category': 'inventory',
    'version': '14.0.1.0.0',
    'depends': ['stock'],
    'data': [
        'views/inventory_adjustment.xml',
    ],
}