# -*- coding: utf-8 -*-

{
    'name': 'Selsela Open HRMS Leave Multi-Level Approval',
    'version': '17.0.1.0.0',
    'summary': """Multilevel Approval for Leaves""",
    'description': 'Multilevel Approval for Leaves, leave approval, '
                   'multiple leave approvers, leave, approval',
    'category': 'Generic Modules/Human Resources',
    'author': "Selsela",
    'company': 'Selsela',
    'website': "",
    'depends': ['base_setup', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'security/selsela_hr_holiday_approval_security.xml',
        'views/hr_leave_views.xml',
        'views/hr_leave_type_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
