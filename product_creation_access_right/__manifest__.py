# -*- coding: utf-8 -*-
{
    'name': "Product Creation",
    'summary': """
        Group give access right to only specific user to create product. 
        """,
    'description': """
    """,
    'author':'A2A Digital''Jenny Sun',
    'category': 'Extral Tools',
    'version': '14.0.1.0.0',
    'depends': ['base','product','stock','purchase','sale','mrp','account'],
    'data': [
                
                'views/product_group_creation.xml',
                'security/ir.model.access.csv',
            ],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
}