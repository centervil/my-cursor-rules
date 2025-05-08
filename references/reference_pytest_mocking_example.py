# Pytest Mocking Example with monkeypatch and unittest.mock
# Source: project_management_guide.md (section 2.2 自動テスト戦略 - モックとスタブの活用)

import pytest
import requests # For mocking external HTTP requests
from unittest.mock import MagicMock # For more complex mocking scenarios

# --- Example 1: Mocking an external API call using monkeypatch --- #

# Function in your application code that makes an external API call
# (e.g., in my_module.py)
# def my_function_that_calls_api():
#     response = requests.get("https://api.example.com/data")
#     response.raise_for_status() # Raise an exception for bad status codes
#     return response.json()

# To be used in a test file (e.g., test_my_module.py)
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"Error: {self.status_code}")

@pytest.fixture
def mock_api_get_success(monkeypatch):
    """Fixture to mock requests.get to return a successful response."""
    def mock_get(*args, **kwargs):
        print(f"Mocked requests.get called with args: {args}, kwargs: {kwargs}")
        return MockResponse({"key": "value", "source": "mock"}, 200)
    monkeypatch.setattr(requests, "get", mock_get)

@pytest.fixture
def mock_api_get_failure(monkeypatch):
    """Fixture to mock requests.get to return an error response."""
    def mock_get(*args, **kwargs):
        return MockResponse({"error": "not found"}, 404)
    monkeypatch.setattr(requests, "get", mock_get)

# Example usage in a test function:
# def test_my_function_with_mocked_success(mock_api_get_success):
#     # Assume my_function_that_calls_api is imported
#     result = my_function_that_calls_api() 
#     assert result["key"] == "value"
#     assert result["source"] == "mock"

# def test_my_function_with_mocked_failure(mock_api_get_failure):
#     # Assume my_function_that_calls_api is imported
#     with pytest.raises(requests.exceptions.HTTPError):
#         my_function_that_calls_api()


# --- Example 2: Using unittest.mock.MagicMock for more control --- #

# Another function in your application code
# (e.g., in another_module.py)
# class DataProcessor:
#     def __init__(self, data_source):
#         self.data_source = data_source
# 
#     def process_data(self):
#         raw_data = self.data_source.fetch()
#         if raw_data:
#             return f"Processed: {raw_data.upper()}"
#         return "No data to process"

# To be used in a test file (e.g., test_another_module.py)

# def test_data_processor_with_magic_mock():
#     # Create a MagicMock instance for the data_source dependency
#     mock_source = MagicMock()
#     
#     # Configure the mock: what fetch() should return
#     mock_source.fetch.return_value = "sample data"
#     
#     # Instantiate the class under test with the mock
#     # processor = DataProcessor(mock_source) 
#     # result = processor.process_data()
#     
#     # Assert that the mock was called as expected
#     # mock_source.fetch.assert_called_once()
#     # assert result == "Processed: SAMPLE DATA"

# def test_data_processor_no_data(monkeypatch):
#     mock_source = MagicMock()
#     mock_source.fetch.return_value = None # Simulate no data

#     # processor = DataProcessor(mock_source)
#     # result = processor.process_data()

#     # mock_source.fetch.assert_called_once()
#     # assert result == "No data to process"


# Note: The actual functions/classes being tested (my_function_that_calls_api, DataProcessor)
# would reside in your application's source code, not in this reference file.
# This file demonstrates how to set up mocks for them in your test files. 