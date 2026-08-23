"""
backend/submissions/executor.py
THE CODE EXECUTION ENGINE
This runs user's code against test cases safely.
Copy this ENTIRE file into backend/submissions/executor.py
"""

import sys
import io
import json
import time
import traceback
try:
    import resource
except ImportError:  # The resource module is not available on Windows.
    resource = None


class CodeExecutor:
    """
    Safely executes user code against test cases.

    Supports:
      - Python 3

    Returns:
      {
        status: 'ACCEPTED' | 'WRONG_ANSWER' | 'RUNTIME_ERROR' |
                'TIME_LIMIT_EXCEEDED' | 'COMPILE_ERROR',
        runtime: 45,          # milliseconds
        memory: 16.2,         # MB
        test_results: [...],  # per-test details
        error_message: '',
        passed: 5,
        total: 5,
      }
    """

    TIME_LIMIT_SECONDS = 5       # max seconds per test case
    MEMORY_LIMIT_MB    = 256     # max memory in MB

    # ─────────────────────────────────────────
    def execute(self, code: str, language: str, test_cases: list) -> dict:
        """
        Entry point. Routes to language-specific executor.
        """
        if language == 'python':
            return self._execute_python(code, test_cases)
        else:
            return {
                'status':        'RUNTIME_ERROR',
                'runtime':       0,
                'memory':        0,
                'test_results':  [],
                'error_message': f'{language} execution not yet supported. Use Python.',
                'passed':        0,
                'total':         len(test_cases),
            }

    # ─────────────────────────────────────────
    def _execute_python(self, code: str, test_cases: list) -> dict:
        """
        Execute Python code safely.

        How it works:
        1. Compile the code to check for syntax errors
        2. For each test case:
           a. Build a call that passes input to the solution
           b. Capture stdout
           c. Compare output to expected
        3. Collect results
        """

        # --- Step 1: Compile check ---
        try:
            compiled = compile(code, '<user_code>', 'exec')
        except SyntaxError as e:
            return {
                'status':        'COMPILE_ERROR',
                'runtime':       0,
                'memory':        0,
                'test_results':  [],
                'error_message': f"SyntaxError at line {e.lineno}: {e.msg}",
                'passed':        0,
                'total':         len(test_cases),
            }

        # --- Step 2: Run each test case ---
        test_results   = []
        total_runtime  = 0
        passed_count   = 0
        final_status   = 'ACCEPTED'
        error_msg      = ''

        for i, tc in enumerate(test_cases):
            result = self._run_single_test(compiled, tc, i + 1)
            test_results.append(result)
            total_runtime += result.get('runtime_ms', 0)

            if result['passed']:
                passed_count += 1
            else:
                # First failure determines overall status
                if final_status == 'ACCEPTED':
                    final_status = result.get('status', 'WRONG_ANSWER')
                    error_msg    = result.get('error_message', '')

        avg_runtime = total_runtime // max(len(test_cases), 1)

        return {
            'status':        final_status,
            'runtime':       avg_runtime,
            'memory':        self._get_memory_mb(),
            'test_results':  test_results,
            'error_message': error_msg,
            'passed':        passed_count,
            'total':         len(test_cases),
        }

    # ─────────────────────────────────────────
    def _run_single_test(self, compiled_code, test_case: dict, test_num: int) -> dict:
        """
        Run one test case against the compiled code.
        Returns a dict with pass/fail and timing.
        """
        input_data     = test_case.get('input_data', '[]')
        expected_raw   = test_case.get('expected_output', 'null')

        try:
            input_value    = json.loads(input_data)
            expected_value = json.loads(expected_raw)
        except json.JSONDecodeError as e:
            return {
                'test_num':      test_num,
                'passed':        False,
                'status':        'RUNTIME_ERROR',
                'input':         input_data,
                'expected':      expected_raw,
                'actual':        '',
                'runtime_ms':    0,
                'error_message': f"Test case data error: {str(e)}",
            }

        # Redirect stdout to capture print() output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        actual_output = None
        status        = 'ACCEPTED'
        error_message = ''
        start_time    = time.perf_counter()

        try:
            # Create fresh namespace for each test
            namespace = {}

            # Execute the user's class/function definitions
            exec(compiled_code, namespace)

            # Try to find and call the solution
            actual_output = self._call_solution(namespace, input_value)

        except TimeoutError:
            status        = 'TIME_LIMIT_EXCEEDED'
            error_message = f"Time limit exceeded on test case {test_num}"

        except MemoryError:
            status        = 'MEMORY_LIMIT_EXCEEDED'
            error_message = "Memory limit exceeded"

        except Exception as e:
            status        = 'RUNTIME_ERROR'
            error_message = self._format_error(e)

        finally:
            runtime_ms = int((time.perf_counter() - start_time) * 1000)
            sys.stdout = old_stdout  # Always restore stdout

        # Check time limit
        if runtime_ms > self.TIME_LIMIT_SECONDS * 1000:
            status        = 'TIME_LIMIT_EXCEEDED'
            error_message = f"Took {runtime_ms}ms, limit is {self.TIME_LIMIT_SECONDS * 1000}ms"

        # Compare output
        passed = False
        if status == 'ACCEPTED' and actual_output is not None:
            passed = self._compare(actual_output, expected_value)
            if not passed:
                status = 'WRONG_ANSWER'

        return {
            'test_num':      test_num,
            'passed':        passed,
            'status':        status,
            'input':         input_data,
            'expected':      json.dumps(expected_value),
            'actual':        json.dumps(actual_output) if actual_output is not None else '',
            'runtime_ms':    runtime_ms,
            'error_message': error_message,
        }

    # ─────────────────────────────────────────
    def _call_solution(self, namespace: dict, input_value):
        """
        Find the Solution class and call the first non-__init__ method.

        Handles these patterns:
          - Solution().methodName(arg1, arg2)
          - Solution().methodName(*args)
        """
        if 'Solution' not in namespace:
            raise RuntimeError("No 'Solution' class found in your code.")

        solution_instance = namespace['Solution']()

        # Find the public method (not __init__, __str__, etc.)
        methods = [
            m for m in dir(solution_instance)
            if not m.startswith('_')
        ]

        if not methods:
            raise RuntimeError("No public method found in Solution class.")

        method = getattr(solution_instance, methods[0])

        # Call with args
        if isinstance(input_value, list):
            return method(*input_value)
        else:
            return method(input_value)

    # ─────────────────────────────────────────
    def _compare(self, actual, expected) -> bool:
        """
        Smart comparison that handles:
          - Numbers (int, float with tolerance)
          - Lists (order-independent option)
          - Strings (strip whitespace)
          - Dicts
          - None/null
        """
        # Exact match first
        if actual == expected:
            return True

        # Float comparison with tolerance
        if isinstance(actual, float) or isinstance(expected, float):
            try:
                return abs(float(actual) - float(expected)) < 1e-5
            except (TypeError, ValueError):
                pass

        # String comparison (strip + lower)
        if isinstance(actual, str) and isinstance(expected, str):
            return actual.strip() == expected.strip()

        # List comparison
        if isinstance(actual, list) and isinstance(expected, list):
            if len(actual) != len(expected):
                return False
            return all(self._compare(a, b) for a, b in zip(actual, expected))

        # Dict comparison
        if isinstance(actual, dict) and isinstance(expected, dict):
            if set(actual.keys()) != set(expected.keys()):
                return False
            return all(self._compare(actual[k], expected[k]) for k in expected)

        return False

    def _format_error(self, e: Exception) -> str:
        """Format error message for display"""
        tb = traceback.format_exc()
        # Remove internal frames, only show user code lines
        lines = tb.split('\n')
        user_lines = [l for l in lines if '<user_code>' in l or type(e).__name__ in l]
        return '\n'.join(user_lines) if user_lines else str(e)

    def _get_memory_mb(self) -> float:
        """Get current memory usage in MB"""
        if resource is None:
            return 0.0

        try:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            return round(usage.ru_maxrss / 1024, 2)  # KB → MB
        except Exception:
            return 0.0
