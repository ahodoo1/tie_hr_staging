# -*- coding: utf-8 -*-

{
    'name': 'Selsela  OpenHRMS Employee Info',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': """Adding Advanced Fields In Employee Master""",
    'description': 'This module helps you to add more information in '
                   'employee records.',
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['base', 'hr', 'mail', 'hr_gamification', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_employee_relation_data.xml',
        'data/ir_cron_data.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
