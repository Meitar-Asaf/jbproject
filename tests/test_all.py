import unittest
# Adjust this import as needed
from tests.vacation_facade_tests import VacationFacadeTests
from tests.user_facade_tests import UserFacadeTests

def test_all():
    loader = unittest.TestLoader()

    # Load specific test cases (e.g., VacationFacadeTests)
    suite = loader.loadTestsFromTestCase(VacationFacadeTests)

    # Run the test suite using a runner
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    suite = loader.loadTestsFromTestCase(UserFacadeTests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
