# -*- coding: utf-8 -*-
{
    'name': "Digitzz",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'project','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/mod.xml',
        'views/wizard.xml',
        'views/menu.xml',
        'views/astask.xml',
        'reports/report.xml',
        'security/security.xml',
    ],

    'installable': True,
    'application': True,
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            'Digitzz/static/src/js/systray_icon.js',
            'Digitzz/static/src/xml/systray_icon.xml',
            'Digitzz/static/src/css/custom.css',
        ],

    },
}
