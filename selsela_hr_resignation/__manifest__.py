# -*- coding: utf-8 -*-

{
    'name': 'Selsela OpenHRMS Resignation',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': 'Handle the resignation process of the employee',
    'description': """To handle the resignation of the employee.It Easily 
    create, manage, and track employee resignations""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': '',
    'depends': ['hr', 'selsela_hr_employee_updation', 'mail'],
    'data': [
        'security/hr_resignation_security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/ir_sequence_data.xml',
        'views/hr_employee_views.xml',
        'views/hr_resignation_views.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
