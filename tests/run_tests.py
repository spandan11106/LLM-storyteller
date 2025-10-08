# run_tests.py

import unittest

if __name__ == '__main__':
    """
    Discovers and runs all tests in the 'tests/' directory.
    This provides a single command to validate the entire application.
    """
    # Create a TestLoader instance
    loader = unittest.TestLoader()
    
    # Discover all tests in the 'tests' directory
    # The pattern 'test*.py' will find any file starting with 'test'
    suite = loader.discover('tests', pattern='test_*.py')
    
    # Create a TestResult runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the test suite
    result = runner.run(suite)
    
    # Optionally, you can exit with a status code indicating success or failure
    # This is useful for automation and CI/CD pipelines
    if result.wasSuccessful():
        print("\n✅ All tests passed successfully!")
        exit(0)
    else:
        print("\n❌ Some tests failed.")
        exit(1)