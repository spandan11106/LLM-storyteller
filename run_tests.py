# run_tests.py

import unittest
import time
from dotenv import load_dotenv

class RichTestResult(unittest.TextTestResult):
    """A custom test result class that captures successes and timings."""
    def __init__(self, *args, **kwargs):
        super(RichTestResult, self).__init__(*args, **kwargs)
        self.successes = []
        self.test_timings = {}

    def startTest(self, test):
        self.test_timings[test.id()] = time.time()
        super(RichTestResult, self).startTest(test)

    def addSuccess(self, test):
        super(RichTestResult, self).addSuccess(test)
        self.successes.append(test)

def generate_report(result):
    """Generates and prints a detailed, contextual report from the test result."""
    report = "\n\n========================================\n"
    report += "        🧪 AI Storyteller Test Report 🧪\n"
    report += "========================================\n"

    total_run = result.testsRun
    start_time = result.test_timings.get('start_time', 0)
    end_time = time.time()

    report += f"\n**Summary:** Ran {total_run} tests in {end_time - start_time:.2f} seconds.\n"
    
    report += "\n--- DETAILED BREAKDOWN ---\n"
    
    all_tests = result.successes + [item[0] for item in result.failures] + [item[0] for item in result.errors]

    for test in sorted(all_tests, key=lambda x: x.id()):
        test_id = test.id()
        status_icon = "✅"
        if test in [item[0] for item in result.failures]:
            status_icon = "❌"
        elif test in [item[0] for item in result.errors]:
            status_icon = "💥"

        # --- FIX: Read the full docstring directly from the test method ---
        doc = test._testMethodDoc or ""
        test_type, comment = "general", "No description."
        if ":" in doc:
            try:
                test_type, comment = doc.split(":", 1)
                comment = comment.strip()
            except ValueError:
                pass

        line = f"{status_icon} [{test_type.upper()}] {test.id().split('.')[-1]}: {comment}"
        
        if test_type == "performance" and status_icon == "✅":
            timing = result.test_timings.get(test_id, 0)
            run_time = time.time() - timing if timing else 0
            # This timing is tricky because of async tests. Let's use a simpler approach.
            # We will use the latency calculated inside the test itself for the report.
            # This requires a slight modification to the performance test.
            
        report += line + "\n"

    if result.failures or result.errors:
        report += "\n--- FAILURES & ERRORS ---\n"
        for test, traceback in result.failures:
            report += f"\n❌ **FAIL:** {test.id()}\n```\n{traceback}\n```\n"
        for test, traceback in result.errors:
            report += f"\n💥 **ERROR:** {test.id()}\n```\n{traceback}\n```\n"

    report += "\n========================================\n"
    if result.wasSuccessful():
        report += "✅ **Verdict: All tests passed successfully!**\n"
    else:
        report += "❌ **Verdict: Some tests failed.**\n"
        
    print(report)


if __name__ == '__main__':
    """
    Discovers and runs all tests, then generates a detailed report.
    """
    load_dotenv()
    
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(resultclass=RichTestResult, verbosity=0)
    
    print("--- Running Full Test Suite ---")
    result = runner.run(suite)
    result.test_timings['start_time'] = time.time() # Store start time for total duration
    
    generate_report(result)
    
    if not result.wasSuccessful():
        exit(1)