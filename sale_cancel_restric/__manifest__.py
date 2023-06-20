# -*- coding: utf-8 -*-
{
    'name': "Sale Cancel Restric",
    'summary': """
        Restrick Sale Person not to Cancel SO if Stock Picking is Done. 
        """,
    'description': """
        
    """,
    'category': 'Extral Tools',
    'version': '14.0.1.0.0',
    'depends': ['base','sale','sale_delivery_state',],
    'data': [
                
                'views/sale_cancel.xml',
                'security/ir.model.access.csv',
            ],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
}
