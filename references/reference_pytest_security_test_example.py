# Pytest Security Test Examples
# Source: pytest_best_practices.md (Section 7.3 Specific Test Examples)

import pytest
from unittest.mock import MagicMock, patch

# Assume these are functions/classes in your application code (e.g., in app/utils.py or app/views.py)
# For demonstration, they are simplified here.

# --- Example Target Functions/Classes (Illustrative) --- #

class User:
    def __init__(self, username, role="user"):
        self.username = username
        self.role = role

    def has_permission(self, permission_name):
        if self.role == "admin":
            return True
        if self.role == "editor" and permission_name in ["edit_article", "view_article"]:
            return True
        if self.role == "user" and permission_name == "view_article":
            return True
        return False

def render_comment_unsafe(comment_text):
    """Simulates rendering a comment without proper XSS sanitization."""
    return f"<div>{comment_text}</div>"

def get_user_by_id_unsafe(db_conn, user_id_str):
    """Simulates an unsafe DB query susceptible to SQL injection."""
    query = f"SELECT * FROM users WHERE id = {user_id_str}" # Unsafe direct formatting
    # In a real scenario, db_conn.execute(query) would run
    print(f"Executing SQL: {query}")
    if user_id_str == "1 OR 1=1": # Simplified mock for successful SQLi
        return {"id": 0, "username": "admin_via_sqli", "is_admin": True} 
    if user_id_str.isdigit() and int(user_id_str) == 1:
         return {"id": 1, "username": "testuser", "is_admin": False}
    return None

class AppConfig:
    DEBUG_MODE = False # Default safe value

    def __init__(self, debug_override=None):
        if debug_override is not None:
            self.DEBUG_MODE = debug_override

# --- Pytest Security Test Examples --- #

# Located in e.g. tests/security/test_security_input_validation.py
@pytest.mark.security
@pytest.mark.parametrize("malicious_comment, description", [
    ("<script>alert('XSS');</script>", "Simple XSS payload"),
    ("<img src=x onerror=alert('XSS')>", "Image XSS payload"),
    ("<b>Safe comment</b>", "Benign HTML (should ideally be escaped or stripped too)")
])
def test_security_xss_in_comment_rendering(malicious_comment, description):
    """Tests if comment rendering is vulnerable to XSS."""
    # ARRANGE: No specific arrangement beyond the input.
    # ACT
    rendered_output = render_comment_unsafe(malicious_comment)
    
    # ASSERT: 
    # A robust test would check that sanitization occurred.
    # For this unsafe function, we might check if the payload is present (undesirable).
    # A better assertion would be: assert "<script>" not in rendered_output_after_sanitization
    if "<script>" in malicious_comment or "onerror" in malicious_comment:
        assert malicious_comment in rendered_output, f"Payload should be present for {description} in unsafe function"
        print(f"Potentially unsafe rendering for {description}: {rendered_output}")
    else:
        assert malicious_comment in rendered_output # Benign HTML check
    # Ideally, this test would be against a *sanitized* version and assert the malicious parts are GONE.

# Located in e.g. tests/security/test_security_sqli.py
@pytest.mark.security
@pytest.mark.parametrize("user_id_input, should_find_admin, description", [
    ("1", False, "Legitimate user ID"),
    ("1 OR 1=1", True, "Classic SQL Injection payload"),
    ("' OR '1'='1' --", True, "SQL Injection with comment"),
    ("1; DROP TABLE users; --", False, "Destructive SQLi (should be caught by ORM or validation ideally)")
])
def test_security_sql_injection_in_user_lookup(user_id_input, should_find_admin, description):
    """Tests user lookup for SQL injection vulnerabilities."""
    # ARRANGE
    mock_db_conn = MagicMock() # Mock the database connection
    # Simulate the db.execute().fetchone() or similar behavior if needed for more complex mocks
    mock_db_conn.execute = lambda query: print(f"Mock DB executing: {query}")

    # ACT
    user_record = get_user_by_id_unsafe(mock_db_conn, user_id_input)

    # ASSERT
    if should_find_admin:
        assert user_record is not None, f"SQLi should have found a record for: {description}"
        assert user_record.get("username") == "admin_via_sqli", f"SQLi should return admin for: {description}"
    elif user_id_input == "1":
        assert user_record is not None
        assert user_record.get("username") == "testuser"
    else:
        # For other non-admin-finding SQLi or legitimate non-finding IDs
        # Depending on how get_user_by_id_unsafe is implemented for non-matches
        # This might be `assert user_record is None` if the mock returns None for failed SQLi
        # or for legitimate IDs not matching the "admin_via_sqli" or "testuser" cases in the mock.
        # The current mock `get_user_by_id_unsafe` returns None for unhandled inputs.
        assert user_record is None, f"Expected no record or non-admin for: {description}, got {user_record}"

# Located in e.g. tests/security/test_security_authorization.py
@pytest.mark.security
@pytest.mark.parametrize("user_role, permission_to_check, expected_result, description", [
    ("admin", "edit_article", True, "Admin should edit articles"),
    ("admin", "delete_user", True, "Admin should delete users (assuming has_permission implies this for admin)"),
    ("editor", "edit_article", True, "Editor should edit articles"),
    ("editor", "view_article", True, "Editor should also view articles"),
    ("editor", "delete_user", False, "Editor should NOT delete users"),
    ("user", "view_article", True, "User should view articles"),
    ("user", "edit_article", False, "User should NOT edit articles"),
    ("guest", "view_article", False, "Guest should NOT have any permissions (by default)")
])
def test_security_role_based_access_control(user_role, permission_to_check, expected_result, description):
    """Tests role-based access control logic."""
    # ARRANGE
    user = User("test_user_for_rbac", role=user_role)
    # ACT
    has_access = user.has_permission(permission_to_check)
    # ASSERT
    assert has_access == expected_result, description

# Located in e.g. tests/security/test_security_configuration.py
@pytest.mark.security
@patch('__main__.AppConfig.DEBUG_MODE', False) # Ensure default is False for most tests
def test_security_debug_mode_not_exposed_in_prod_config(MockedDebugMode):
    """Verifies DEBUG_MODE is False by default or in a 'production' config."""
    # ARRANGE: Mocked to False via @patch
    # ACT
    config = AppConfig()
    # ASSERT
    assert config.DEBUG_MODE is False, "DEBUG_MODE should be False in production"

@pytest.mark.security
def test_security_debug_mode_can_be_enabled_for_testing_explicitly():
    """Verifies DEBUG_MODE can be True if explicitly set for testing purposes."""
    # ARRANGE
    # ACT
    config = AppConfig(debug_override=True)
    # ASSERT
    assert config.DEBUG_MODE is True, "DEBUG_MODE should be True when explicitly overridden for testing"

# Note: To run these tests, you would save this content into the respective
# files within your `tests/security/` directory, and ensure the application code
# (User, render_comment_unsafe, get_user_by_id_unsafe, AppConfig) is importable.
# These examples are simplified; real-world tests would often involve more complex setup,
# fixtures (e.g., for a test client or database session), and more sophisticated mocking. 