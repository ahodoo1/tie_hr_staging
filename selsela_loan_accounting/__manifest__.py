# -*- coding: utf-8 -*-

{
    'name': 'Selsela OpenHRMS Loan Accounting',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': 'Open HRMS Loan Accounting',
    'description': """Manage Loan Request of Employees.Double Layer Approval 
     of Hr Department and Accounting.Create accounting entries for loan 
     requests.""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': [
        'hr_payroll',
        'hr',
        'account',
        'account_accountant',
        'selsela_ohrms_loan'
    ],
    'data': [
        'views/hr_loan_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
