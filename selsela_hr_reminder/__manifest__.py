# -*- coding: utf-8 -*-

{
    'name': 'OpenHRMS Reminders Todo',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'HR Reminder For OHRMS',
    'description': """This module is a powerful and easy-to-use tool that can 
    help you improve your HR processes and ensure that important events are 
    never forgotten.""",
    'author': 'Selsela',
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['hr'],
    'data': [
        'security/hr_reminder_security.xml',
        'security/ir.model.access.csv',
        'views/hr_reminder_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'selsela_hr_reminder/static/src/css/notification.css',
            'selsela_hr_reminder/static/src/scss/reminder.scss',
            'selsela_hr_reminder/static/src/xml/reminder_topbar.xml',
            'selsela_hr_reminder/static/src/js/reminder_topbar.js',
        ],
    },
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
