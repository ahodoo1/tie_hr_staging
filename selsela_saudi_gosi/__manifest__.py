# -*- coding: utf-8 -*-

{
    'name': "Selsela Open HRMS GOSI",
    'version': '17.0.1.0.0',
    'category': 'Human Resource',
    'summary': """GOSI Contribution for Saudi Government""",
    'description': """Module Helps to Manage Payslips Including GOSI 
    Contribution for Saudi Government From Employee and Company""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['hr', 'selsela_ohrms_loan', 'hr_payroll'],
    'data': [
             'security/ir.model.access.csv',
             'data/hr_payroll_structure_data.xml',
             'data/hr_salary_rule_data.xml',
             'data/ir_sequence_data.xml',
             'views/gosi_payslip_views.xml',
             'views/hr_employee_views.xml',
             'views/hr_payslip_views.xml',
            ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
