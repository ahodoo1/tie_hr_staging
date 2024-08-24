# -*- coding: utf-8 -*-

{
    'name': 'Selsela OpenHRMS Loan Management',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': 'Manage Loan Requests',
    'description': """Helps you to manage Loan Requests of your company's 
     staff.""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': [
        'base', 'hr_payroll', 'hr', 'account',
    ],
    'data': [
        'security/hr_loan_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/hr_salary_rule_data.xml',
        'data/hr_payslip_input_type_data.xml',
        'views/hr_employee_views.xml',
        'views/hr_loan_views.xml',
        'views/hr_payroll_structure_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_salary_rule_views.xml'
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
