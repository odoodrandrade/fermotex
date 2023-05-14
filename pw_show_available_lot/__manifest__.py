# -*- coding: utf-8 -*-
{
    'name': 'Show Available Lot on Delivery | Hide Unavailable Product Lot on Delivery',
    'version': '1.0',
    'author': 'Preway IT Solutions',
    'category': 'Warehouse',
    'depends': ['stock'],
    'summary': 'This apps helps you to only show available lots/serial on delivery order | Hide zero lot on delivery | Hide zero serial on delivery | hide not available lot on picking',
    'description': """
Hide Unavailable Product Lot on Delivery.
    """,
    'data': [
        'views/stock_move_line_views.xml',
    ],
    'price': 10.0,
    'currency': "EUR",
    'application': True,
    'installable': True,
    "license": "LGPL-3",
    "images":["static/description/Banner.png"],
}
