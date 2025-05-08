# Pytest Parameterized Test Example
# Source: project_management_guide.md (section 2.2 自動テスト戦略 - パラメータ化テスト)

import pytest

# --- Example 1: Simple Parameterization --- #

# Function to be tested (e.g., in your_module.py)
# def convert_text(text_input: str) -> str:
#     if text_input == "text1":
#         return "RESULT1"
#     elif text_input == "text2":
#         return "RESULT2"
#     elif text_input == "text3":
#         return "RESULT3"
#     return "UNKNOWN"

# Test function using parameterization (e.g., in test_your_module.py)
@pytest.mark.parametrize("input_val, expected_output", [
    ("text1", "RESULT1"),
    ("text2", "RESULT2"),
    ("text3", "RESULT3"),
    ("other", "UNKNOWN"),
    ("", "UNKNOWN"), # Test with empty string
])
def test_convert_text_parameterized(input_val, expected_output):
    """Tests the convert_text function with multiple inputs."""
    # from your_module import convert_text # Assuming convert_text is imported
    # assert convert_text(input_val) == expected_output
    pass # Placeholder if convert_text is not actually defined here

# --- Example 2: Parameterizing with Test IDs --- #

# Another function to be tested (e.g., in validation_utils.py)
# def is_valid_email(email: str) -> bool:
#     if not email or "@" not in email or "." not in email.split("@")[-1]:
#         return False
#     return True

@pytest.mark.parametrize(
    "email_candidate, expected_validity",
    [
        pytest.param("test@example.com", True, id="valid-simple"),
        pytest.param("test.user+alias@example.co.uk", True, id="valid-complex"),
        pytest.param("invalid", False, id="invalid-no_at_symbol"),
        pytest.param("invalid@domain", False, id="invalid-no_dot_in_domain"),
        pytest.param("@example.com", False, id="invalid-no_local_part"),
        pytest.param("", False, id="invalid-empty_string"),
    ]
)
def test_is_valid_email_parameterized(email_candidate, expected_validity):
    """Tests email validation with various cases and custom test IDs."""
    # from validation_utils import is_valid_email # Assuming is_valid_email is imported
    # assert is_valid_email(email_candidate) == expected_validity
    pass # Placeholder

# --- Example 3: Combining Fixtures with Parameterization --- #

@pytest.fixture
def base_url():
    return "https://api.myapp.com/v1"

@pytest.mark.parametrize("endpoint, params, expected_status", [
    ("/users", {"active": True}, 200),
    ("/products", {"category": "electronics"}, 200),
    ("/orders", {"user_id": 123, "status": "pending"}, 200),
    ("/nonexistent", {}, 404),
])
def test_api_endpoints(base_url, endpoint, params, expected_status):
    """Tests various API endpoints using a base_url fixture and parameterization."""
    full_url = f"{base_url}{endpoint}"
    print(f"Simulating request to: {full_url} with params: {params}")
    # In a real test, you would use an HTTP client (possibly mocked or a real one for integration)
    # response_status = make_api_request(full_url, params).status_code
    # assert response_status == expected_status
    pass # Placeholder

# Note: The actual functions being tested (convert_text, is_valid_email) 
# would reside in your application's source code.
# This file demonstrates how to set up parameterized tests for them. 