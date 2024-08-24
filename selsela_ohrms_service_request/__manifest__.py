# -*- coding: utf-8 -*-

{
    'name': "Selsela Open HRMS Service Request",
    'version': '17.0.1.0.0',
    'category': 'Human Resource',
    'summary': """Allow Employees To Raise A Service Request""",
    'description': """Module provides employee service requests, approvers, 
    service reports""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['stock', 'selsela_oh_employee_creation_from_user',
                'project', 'hr_attendance'],
    'data': [
            'security/ir.model.access.csv',
            'security/selsela_ohrms_service_request_security.xml',
            'views/service_request_views.xml',
            'views/service_execution_views.xml',
            'views/ir_sequence.xml',
            ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': True,
    'application': True,
}

