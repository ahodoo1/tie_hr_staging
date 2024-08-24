# -*- coding: utf-8 -*-

{
    'name': 'Selsela Open HRMS Official Announcements',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': """Managing Official Announcements""",
    'description': """This module helps you to manage hr official announcements
     and Add Attachments to the announcement""",
    'author': "Selsela",
    'company': 'Selsela',
    'website': "",
    'maintainer': 'Selsela',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_announcement_security.xml',
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'views/hr_announcement_views.xml',
        'views/hr_employee_views.xml'
    ],
    'demo': ['demo/hr_announcement_demo.xml'],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
