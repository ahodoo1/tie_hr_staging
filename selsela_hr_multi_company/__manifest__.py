# -*- coding: utf-8 -*-

{
    'name': 'Selsela OpenHRMS Multi-Company',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': """Enables Multi-Company""",
    'description': """This module enables HR multi company, hence HR manager 
     can easily handle multi company process separately. We can activate
     multi company feature in general settings as usual. This will
     automatically add company field in every HR related records""",
    'author': "Selsela",
    'company': 'Selsela',
    'website': "",
    'maintainer': 'Selsela',
    'depends': ['base',
                'hr',
                'hr_contract',
                'hr_payroll',
                'hr_expense',
                'hr_attendance',
                'hr_holidays'],
    'data': [
        'security/hr_attendance_security.xml',
        'security/hr_department_security.xml',
        'security/hr_expense_security.xml',
        'security/hr_leave_security.xml',
        'security/hr_payslip_security.xml',
        'security/hr_salary_rule_category_security.xml',
        'views/hr_attendance_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_salary_rule_category_views.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
