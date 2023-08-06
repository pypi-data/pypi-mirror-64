# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class SaleAvailableStockTestCase(ModuleTestCase):
    'Test Sale Available Stock module'
    module = 'sale_available_stock'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleAvailableStockTestCase))
    return suite
