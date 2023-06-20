# -*- coding: utf-8 -*-
{
    'name': "Stock KIT",
    'summary': """
        Overwrite Function _Compute_bom_qty_ In sale
        """,
    'description': """
        - Update of the original code by remove the append function with float_round and precision_rounding
        - Remove the condition check and convert qty_ratios
        - From [min(qty_ratios)//] to qty_ratios
    """,
    'author': "A2A Town Cambodia" "Jenny Sun",
    'category': 'Extral Tools',
    'version': '14.0.1.0.0',
    'depends': ['base','stock',],
    'data': [],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
}
