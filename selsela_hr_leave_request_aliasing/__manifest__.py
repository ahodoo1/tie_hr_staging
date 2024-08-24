# -*- coding: utf-8 -*-

{
    'name': 'Selsela OpenHRMS Leave Request Aliasing',
    'version': '17.0.1.1.0',
    'category': 'Human Resources',
    'summary': 'Allows You To Create Leave Request Automatically From '
               'Incoming Mails.',
    'description': 'This module allows you to create leave request directly '
                   'from incoming mails.',
    'author': 'Selsela',
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['hr_holidays'],
    'data': [
        'data/mail_alias_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
