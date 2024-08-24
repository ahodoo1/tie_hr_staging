
{
    'name': 'Selsela Open HRMS Employee Documents',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': """Manages Employee Documents With Expiry Notifications.""",
    'description': """This module Manages Employee Related Documents with 
     Expiry Notifications.Employee documents with such necessary information 
     must be saved and used accordingly.This module helps to  store and manage
     the employee related documents like certificates, appraisal reports, 
     passport,license etc""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['hr'],
    'data': [
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/hr_document_views.xml',
        'views/document_type_views.xml',
        'views/hr_employee_document_views.xml',
        'views/hr_employee_views.xml',
    ],
    'demo': [
        'data/document_type_demo.xml',
        'data/hr_work_location_demo.xml',
        'data/hr_employee_demo.xml',
        'data/hr_employee_document_demo.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
