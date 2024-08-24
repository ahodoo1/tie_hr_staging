# -*- coding: utf-8 -*-

{
    'name': 'Selsela OpenHRMS Advance Salary',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': 'Advance Salary In HR',
    'description': "Helps you to manage Advance Salary Request of "
                   "your company's staff.",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': [
        'hr',
        'hr_payroll',
        'hr_contract',
        'account_accountant',
        'selsela_ohrms_loan',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/salary_structure.xml',
        'data/ir_sequence_data.xml',
        'views/salary_advance_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}

