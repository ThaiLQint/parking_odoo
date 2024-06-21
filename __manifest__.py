# -*- coding: utf-8 -*-
{
    'name': "PARKING",
    'sequence': 0,

    'summary': """
       Ứng dụng sử dụng cho bãi giữ xe, kế thừa những chức năng của 
       những ứng dụng liên quan đến quản lý Kho.
       """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'NSP',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['contacts','stock', 'product', 'base'],
    "application": True,
    # always loaded
    'data': [
        "views/User.xml",     
        "security/access_user.xml",
        "security/ir.model.access.csv",     
        "security/record_rule.xml",
        "views/AlerTag.xml",
        "views/Contact.xml",
        "views/ProductTemplate.xml",
        "views/StockLocation.xml",
        "views/StockMoveLine.xml",
        "views/SettingNSP.xml",
        "views/product_color_main.xml",
        "views/nsp_menu_setting.xml",     
        "views/hidden_view.xml",     
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': True,
    'assets': {
        'web.assets_backend':
        [
            'parking_odoo/static/src/**/*',
        ],
    },
}
