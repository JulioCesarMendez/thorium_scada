##############################################################################
#
#    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website>
#
##############################################################################

from odoo import ModuleTestCase


class ThoriumcorpScadaTestCase(ModuleTestCase):
    '''
    Test Thorium Corp FP SCADA module.
    '''
    module = 'thoriumcorp_scada'


def suite():
    suite = thorium.tests.test_thorium.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ThoriumcorpScadaTestCase))
    return suite
