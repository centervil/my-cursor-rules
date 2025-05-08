# Pytest Common Commands Reference

This document lists common Pytest commands as referenced in `knowledge_pytest_testing_strategy.mdc` and `project_management_guide.md`.

## Basic Test Execution

- Run all tests in the current directory and subdirectories:
  ```bash
  pytest
  ```

- Run tests in a specific file:
  ```bash
  pytest path/to/your_test_file.py
  ```

- Run a specific test function within a file:
  ```bash
  pytest path/to/your_test_file.py::test_specific_function
  ```

- Run tests marked with a specific marker (e.g., `@pytest.mark.slow`):
  ```bash
  pytest -m slow
  ```

- Stop test execution after the first failure:
  ```bash
  pytest -x
  ```

- Run tests in verbose mode (shows more details):
  ```bash
  pytest -v
  ```

## Code Coverage (with `pytest-cov`)

- Generate a coverage report for the `src/` directory and display it in the terminal:
  ```bash
  pytest --cov=src/
  ```

- Generate an HTML coverage report (typically in `htmlcov/` directory):
  ```bash
  pytest --cov=src/ --cov-report=html
  ```

- Generate an XML coverage report (useful for CI integration):
  ```bash
  pytest --cov=src/ --cov-report=xml:coverage.xml
  ```

## Parallel Test Execution (with `pytest-xdist`)

- Distribute tests across available CPU cores automatically:
  ```bash
  pytest -n auto
  ```

- Distribute tests across a specific number of workers (e.g., 4):
  ```bash
  pytest -n 4
  ```

## Performance Testing (with `pytest-benchmark`)

- Run benchmark tests and save results to a JSON file:
  ```bash
  pytest --benchmark-json=benchmark_results.json
  ```

- Calibrate benchmark iterations before running:
  ```bash
  pytest --benchmark-autosave --benchmark-warmup=on
  ```

## Other Useful Options

- Show help for Pytest command-line options:
  ```bash
  pytest -h
  ```

- List all collected tests without running them:
  ```bash
  pytest --collect-only
  ```

- Disable capturing of stdout/stderr (useful for debugging):
  ```bash
  pytest -s
  ``` 