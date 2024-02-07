# -*- coding: utf-8 -*-
{
    "name": "Fleet Payment Method",
    "description": """
        This module provides functionalities:

        - Payment Method.
        - Custom Fleet Service Reports.
    """,
    "author": "Estarling Polanco",
    "website": "https://mepyd.gob.do/",
    "category": "Fleet/Management",
    "version": "15.0.0.1.0",
    "depends": ["base", "fleet", "account", "l10n_do_accounting"],
    "data": [
        "security/ir.model.access.csv",
        "views/method_payment.xml",
        "views/fleet_vehicle_log_services.xml",
        "report/report_fleet_vehicle_log_services.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
