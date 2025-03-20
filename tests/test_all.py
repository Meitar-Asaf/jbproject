


from tests.vacation_facade_tests import VacationFacadeTests
from tests.user_facade_tests import UserFacadeTests

import unittest

def test_all():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(VacationFacadeTests))
    suite.addTests(loader.loadTestsFromTestCase(UserFacadeTests))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
