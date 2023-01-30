# -*- coding: utf-8 -*-
{
    'name': "fermotex",

    'summary': """fermotex modules""",

    'description': "fermotex",

    'author': "Aortiz",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale_management', 'stock', 'account_accountant', 'purchase', 'mail', 'contacts'],
    'images': ['src/img/logo.png'],
    'installable': True,
    'active': True,
    'application': True,
    # 'auto_install': True,
    # 'external_dependencies': {'python' : ["openid"]},
    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        "security/security.xml",
        "views/fermotex_sale_order.xml",
        "views/fermotex_account_move.xml",
        # "views/gemex_proyecto.xml",
        # "views/gemex_fabricacion.xml",
    ],
    'qweb': [],
}
