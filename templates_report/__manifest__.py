# -*- coding: utf-8 -*-
{
    'name': "Templates Report PLM",
    'summary': """ PLM Templates Report""",
    'description': """
        PLM Templates Report for 
        - Sale, 
        - tclearance, 
        - transportation, 
        - concrete and concrete with tax 
        - vendor bill
        - advance expense transport
        - quotation & pro_forma invoice in sale
    """,
    'author': "Jenny Sun ",
    'category': 'Extra Tool',
    'version': '14.0.1.0.0',
    'depends': ['account','purchase'],
    'data': [
        'views/web.xml',
        'reports/report_purchase_order.xml',
        'reports/report_vendor_bill.xml',
        'reports/report_advance_expense_transport.xml',
        'reports/report_pro_forma_invoice.xml',
        'reports/report_quotation_sale.xml',
        'reports/report_tax_invoice_concrete.xml',
        'reports/report_tax_invoice_by_government.xml',
        'reports/report_tax_invoice_commercial.xml',
        'reports/report_other_income_receipt.xml',
        'reports/report_tclearance_invoice.xml',        
        'reports/report_sale_invoice.xml',
        'reports/report_concrete_invoice.xml',
        'reports/report_transportation_invoice.xml',
        'reports/report.xml',
    ],
    'demo': [],
}
