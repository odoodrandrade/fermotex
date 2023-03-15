{
    'name': 'Hide cost Price',
    "author": "Sottosoft Solution",
    'version': '16.0.1',
    "website": "",
    'category': 'Extra Tools',
    "support": "sottosoftsolution@gmail.com",
    'summary': 'Hide Cost Price,Disable cost From Product,Hide cost',
    'description': """
        Hide Cost Price from form view and tree view of Product and its variants.
    """,
    'images': ["static/description/img_1.png"],
    'depends': ['product'],
    'data': [
        'security/hide_cost_group.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'application':True,
    "price": 0,
    "currency": "EUR"
}   
