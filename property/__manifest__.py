# -*- coding: utf-8 -*-
{
    'name': "property",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Usama Fathi",
    'website': "https://www.linkedin.com/in/usama-fathi-4bb282239/",
    'category': 'Hotel Management',
    'version': '17.0.0.1',

    'depends': ['base', 'sale_management', 'account_accountant', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menus.xml',
        'views/property_views.xml',
        'views/owner_views.xml',
        'views/tag_views.xml',
        'views/sale_order_views.xml',
        'views/building_views.xml',
        'views/property_history_views.xml',
        'wizard/change_state_wizard_views.xml',
        'reports/property_report.xml',
    ],
    'assets': {
        'web.assets_backend': ['property/static/src/css/property.css'] ,
        'web.report.assets_common': ['property/static/src/css/fonts.css'],
    },
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
