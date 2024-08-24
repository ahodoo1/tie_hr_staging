# -*- coding: utf-8 -*-

{
    'name': 'Selsela HRMS Employee Background Verification',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': """Verify the background details of an Employee """,
    'description': 'Manage the employees background verification Process '
                   'employee verification ',
    'author': 'Selsela',
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['hr_recruitment', 'mail',
                'selsela_hr_employee_updation', 'contacts', 'portal', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/default_mail.xml',
        'views/employee_verification_views.xml',
        'views/res_partner_views.xml',
        'views/agent_portal_templates.xml',
    ],
    'demo': ['data/employee_background_data.xml'],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
