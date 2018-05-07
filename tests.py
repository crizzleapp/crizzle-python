import unittest

# Import test case modules (or parent modules)
from crizzle import services, envs, patterns

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add test cases to suite
suite.addTests(loader.loadTestsFromModule(services.binance.test_service))


# Run tests
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
