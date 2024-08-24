# -*- coding: utf-8 -*-

{
    'name': 'Selsela Open HRMS Company Transfer',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'This module is used to transfer employee between companies',
    'description': 'Transferring employees between company is a basic thing in an '
                   'organization. Odoo lacks a provision for employee transfer. '
                   'This module gives a basic structure for employee transfer.'
                   'Make sure that your multi company is enabled.',
    'author': 'Selsela',
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': '',
    'depends': ['hr_contract', 'selsela_hr_employee_updation'],
    'data': [
        'security/ir.model.access.csv',
        'security/company_security.xml',
        'views/employee_transfer_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
