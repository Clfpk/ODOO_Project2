# -- coding: utf-8 --
{
    'name': 'real_estate',
    'author': 'Cloudinfosoft',
    'version': '17.0',
    'license': 'LGPL-3',
    'sequence': 1,
    'category': 'REAL ESTATE',
    'depends': ['base','account'],
    'data': ['security\ir.models.access.csv',
             'view\estate_property_type.xml',
             'view\property.xml'],
    'auto_install': False,
    'application': True,
    'installable': True,
}