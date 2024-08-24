# -*- coding: utf-8 -*-

{
    'name': 'Selsela Open HRMS Custody',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Manage the company properties when it is in the 
    custody of an employee""",
    'description': 'Manage the company properties when it is in the '
                   'custody of an employee',

    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['base', 'hr', 'mail', 'selsela_hr_employee_updation', 'product',
                'stock'],
    'data': [
        'security/custody_property_security.xml',
        'security/hr_custody_security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'views/hr_custody_views.xml',
        'views/hr_employee_views.xml',
        'views/custody_property_views.xml',
        'report/report_custody_views.xml',
    ],
    'demo': ['data/demo_data.xml'],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
