# -*- coding: utf-8 -*-
{
    'name': "gestion_zoo",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'images': ['gestion_zoo/static/description/icon.png'], 

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/animales.xml',
        'views/chequeomedico.xml',
        'views/continentes.xml',
        'views/cuidadores.xml',
        'views/especies.xml',
        'views/estadoslaborales.xml',
        'views/habitaculos.xml',
        'views/tipocomida.xml',
        'views/wizards.xml',
        'views/empresas.xml',
        'views/locales.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gestion_zoo/static/src/css/style.css',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

