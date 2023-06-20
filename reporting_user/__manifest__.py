{
    'name': "reporting_normal_user",
    'summary': """Access right for Reporting menu for Normal User""",
    'description': """ Access right for Normal User can see Reporting:
            - Inventory
            - Sale
            - Purchase
            """,
    'author': "A2A Digital",
    'category': 'Extra Tools',
    'version': '14.0.1.0.0',
    'depends': ['stock','sale','purchase',],
    'data': [
        'views/reporting_menu.xml',
    ]
}