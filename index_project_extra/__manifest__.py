# -*- coding: utf-8 -*-
{
    'name': "Project Extra (Index)",

    'description': """
        Funcionalidades extra a Projecto para Index Occidente.
    """,

    'author': "SIE Center / Samuel Santana",
    'website': "http://www.siecenter.com.mx",
   
    'version': '15.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['project'],

    # always loaded
    'data': [
        'views/project_task.xml',
        'views/custom_task_line.xml',
        'data/container_types.xml',
        'data/packing_types.xml',
        'data/service_types.xml',
        'security/ir.model.access.csv',

    ],
}
