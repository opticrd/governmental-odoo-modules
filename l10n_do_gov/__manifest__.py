# -*- coding: utf-8 -*-

# Author: Gustavo Valverde <gvalverde@iterativo.io>
# Contributors: Kevin Jiménez - <kevin.jimenez@ogtic.gob.do>

# Copyright (c) 2022 - Present
# All rights reserved.

{
    'name': 'Dominican Republic - Govermental Accounting',
    'version': '15.0.1.0.3',
    'category': 'Accounting/Localizations/Account Charts',
    'summary': """

Localization Module for Dominican Republic Goverment
=====================================================
Description pending

    """,
    'author': 'Gustavo Valverde',
    'website': 'http://ogtic.gob.do',
    'depends': ['account',
                'purchase',
                'sale',
                'stock',
                'base_iban',
                'product_analytic',
                ],
    'data': [
        # Basic accounting data
        'data/l10n_do_gov_chart_data.xml',
        'data/account.group.template.csv',
        'data/account.account.template-common.csv',
        'data/account.account.template.csv',
        'data/account_chart_template_data.xml',
        'data/account_tax_group_data.xml',
        'data/account_tax_report_data.xml',
        'data/account.tax.template.xml',
        # configuration wizard, views, reports...
        'data/account_chart_template_configure_data.xml',
        # Extra master data
        'data/masters/account_analytic_group.xml',
        'data/masters/account_analytic_account.xml',
        'data/masters/product_category.xml',
        'data/masters/product_product.xml',

    ],
    'demo': [
        # 'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
