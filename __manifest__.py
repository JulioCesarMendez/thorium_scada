#
#    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website>
#

{
    'name': "Thorium Corp SCADA Web",
    'summary': """
        Thorium Corp SCADA Web Module
    """,
    'description': """
        Thorium Corp SCADA Web Module (Under development) 
        ################################

        This modules includes monitoring metods for:

            * On line Values, Alarm, Events, Messages, actions valvs, etc (Analog & Digital)
            * Reports
            * Graphics
    """,
    'author': "Thorium Corp FP",
    'website': "https://thoriumcorp.website",
    'category': 'Thoriumcorp',
    'version': '12.0.0.0.1',
    'depends': [],
    'data': [
#        'security/ir.model.access.csv',
#        'views/thoriumcorp_partner.xml',
        'views/thoriumcorp_scada_web_flash.xml',
        # 'security/access_rights.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'maintainer': 'Julio César Méndez <mendezjcx@thoriumcorp.website>'
}
