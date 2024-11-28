{
    "name": "Purchase Price History",
    "summary": """
        Record products (and services) purchase price history.
        
        This works as product and service price database for future consulting when an organization needs price reference to begin a new purchase process in the future.
    """,
    "author": "José López, OGTIC",
    "website": "https://ogtic.gob.do",
    "category": "Purchase",
    "version": "15.0.0.1.0",
    "depends": ["purchase"],
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/server_action_data.xml",
        "views/product_price_history_views.xml",
    ],
    "installable": True,
}
