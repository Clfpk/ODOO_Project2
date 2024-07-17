# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'rel_pos_werafoods',
    'version': '1.2',
    'summary': 'Point of Sale Related changes',
    'sequence': 10,
    'description': """   """,
    'category': '',
    'website': '',
    'depends': ['base', 'point_of_sale', 'web', 'pos_restaurant', 'pos_self_order'],
    'data': [
        'security/security_rights.xml',
        'views/pos_category_views.xml',
        'views/report_saledetails.xml',
        'views/pos_order_view.xml',
        'views/pos_order_report_view.xml',
        'views/pos_change_title.xml',
        'views/favicon.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'rel_pos_customization/static/src/**/*',
            'rel_pos_customization\static\src\store\models\discount_button\discount_button.js',
            'rel_pos_customization\static\src\store\models\discount_button\discount_button.xml'
        ],
        'web.assets_frontend': [
        ],
    },
    'license': 'LGPL-3',
}
