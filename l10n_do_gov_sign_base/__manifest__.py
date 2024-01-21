{
    "name": "Firmas Gov Base",
    "summary": """
        Base module for Firmas Gov instegration features
    """,
    "author": "José López, OGTIC",
    "website": "https://optic.gob.do",
    "category": "Uncategorized",
    "version": "15.0.1.0.0",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_config_parameter_data.xml",
        "views/res_users_views.xml",
        "wizard/l10n_do_gov_sign_request_wizard_views.xml",
    ],
}
