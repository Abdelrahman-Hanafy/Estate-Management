{
    'name': "Estate Management",
    'version': '1.0',
    'depends': ['base'],
    'author': "Abdelrahman Hanafy",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/owner_views.xml',
        'views/tenant_views.xml',
        'views/property_views.xml',
        'views/property_document.xml',
        'views/transaction_view.xml',
        'views/contract_views.xml',
        'views/estate_management_menu.xml',

    ],
    'application': True,
}
