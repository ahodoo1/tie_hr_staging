# -*- coding: utf-8 -*-

{
    'name': 'Selsela OpenHRMS Employees From User',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': 'Automatically Creates Employee While Creating User',
    'description': """This module helps you to create employees automatically 
     while creating users""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['base', 'hr'],
    'data': [
        'views/res_users_views.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
