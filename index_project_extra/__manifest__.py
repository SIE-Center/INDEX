# -*- coding: utf-8 -*-
{
    'name': "Project Extra (Index)",

    'description': """
        Funcionalidades extra a Projecto para Index Occidente.
    """,

    'author': "SIE Center / Samuel Santana",
    'website': "http://www.siecenter.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
   
    'version': '15.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': [
    'project',
    #'res',
    ],

    # always loaded
    'data': [
        'views/project_task.xml',
        'views/custom_task_line.xml',
        'views/res_partner.xml',
        'views/project_stage.xml',
        'views/extra_models.xml',
        'views/validations.xml',
        'views/rep_conf.xml',
        'wizard/rep_eta_day.xml',
        'data/container_types.xml',
        'data/packing_types.xml',
        'data/service_types.xml',
        'security/ir.model.access.csv',
        'security/security.xml',

    ],
}
