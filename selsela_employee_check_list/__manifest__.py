# -*- coding: utf-8 -*-

{
    'name': 'Selsela Open HRMS Employee Checklist',
    'version': '17.0.1.0.0',
    'summary': """Manages Employee's Entry & Exit Process""",
    'description': """This module is used to remembering the employee's entry and exit progress.""",
    'category': 'Human Resources',
    'author': 'Selsela',
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['selsela_employee_documents_expiry', 'mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/checklist_views.xml',
        'views/employee_check_list_views.xml',
        'views/hr_employee_views.xml',
        'views/mail_activity_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}

