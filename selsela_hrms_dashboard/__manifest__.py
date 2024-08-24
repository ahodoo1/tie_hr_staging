# -*- coding: utf-8 -*-

{
    'name': "Selsela Open HRMS - HR Dashboard",
    'version': '17.0.1.0.1',
    'category': 'Generic Modules/Human Resources',
    'summary': """Open HRMS HR dashboard,facilitates with various 
     metrics helping easy to view, understand, and share data.Experience the 
     new kind of responsiveness with Open HRMS Dashboard""",
    'description': """Human Resource Departments have a lot to manage and 
     volume to track with reports ever growing. Fortunately, technologies 
     provide elegant solutions to track and monitor every essential Human 
     Resource activities. Open HRMS HR Dashboard provides a visually engaging
     palate for seamless management of Human Resource functions. It provides
     executives and employees the information they need. Open HRMS Dashboard 
     comes intuitive and interactive connecting every dots of your data like 
     never before. With Open HRMS HR dashboard,facilitates with various 
     metrics helping easy to view, understand, and share data.Experience the 
     new kind of responsiveness with Open HRMS Dashboard""",
    'author': "Selsela",
    'company': 'Selsela',
    'maintainer': 'Selsela',
    'website': "",
    'depends': ['hr', 'hr_holidays', 'hr_timesheet', 'hr_payroll',
                'hr_attendance', 'hr_timesheet_attendance',
                'hr_recruitment', 'selsela_hr_resignation', 'event',
                'selsela_hr_reward_warning', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'report/hr_employee_broad_factor_reports.xml',
        'views/hr_leave_views.xml',
        'views/selsela_hrms_dashboard_menus.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'selsela_hrms_dashboard/static/src/css/hrms_dashboard.css',
            'selsela_hrms_dashboard/static/src/css/lib/nv.d3.css',
            'selsela_hrms_dashboard/static/src/js/hrms_dashboard.js',
            'selsela_hrms_dashboard/static/src/js/lib/d3.min.js',
            'selsela_hrms_dashboard/static/src/xml/hrms_dashboard_templates.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js',
        ],
    },
    'external_dependencies': {'python': ['pandas']},
    'images': ["static/description/icon.png"],
    'license': "OPL-1",
    'installable': True,
    'auto_install': False,
    'application': True,
}
