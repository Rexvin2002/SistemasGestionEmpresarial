# -*- coding: utf-8 -*-
{
    'name': "Psicología",
    'summary': """
        Módulo para la gestión de consultas psicológicas, pacientes y tratamientos""",
    'description': """
        Sistema completo para la gestión de una consulta psicológica:
        - Registro de pacientes e historiales clínicos
        - Agenda de citas y seguimiento de tratamientos
        - Evaluaciones psicológicas y reportes
        - Facturación y pagos
    """,
    'author': "Kevin Gómez Valderas",
    'website': "https://www.instagram.com/suval_nnespana/",
    'category': 'Health',
    'version': '1.0.0',

    # Dependencias
    'depends': [
        'base',
        'calendar',  # Para gestión de citas
        'account',   # Para facturación
    ],

    # Archivos de datos
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/Psicologia.xml',
        'views/Paciente.xml',
        'views/Psicologo.xml',
        'views/Sesion.xml',
        'views/Tratamiento.xml',
        'views/Factura.xml',
        'views/Terapia.xml',
        'views/AsignarPacientesWizard.xml',
        'views/CrearTerapiaWizard.xml',
    ],

    
    # Datos de demostración
    'demo': [
        'demo/patient_demo.xml',
        'demo/session_demo.xml',
    ],

    # Configuración
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',

    # Precio (si es comercial)
    'price': 0.0,
    'currency': 'EUR',

    # Soporte
    'support': 'kevin.gomez@example.com',
    'maintainer': 'Kevin Gómez Valderas',

    # Imágenes
    'images': [
        'static/description/icon.png',
        'static/description/main_screenshot.png',
    ],

    # Dependencias externas
    'external_dependencies': {
        'python': [],  # Para análisis de datos
    },
}