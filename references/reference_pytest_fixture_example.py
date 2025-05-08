# Pytest Fixture Example
# Source: project_management_guide.md (section 2.1 Pytestを活用したテスト駆動開発)

import pytest

# Example ApiClient class (assuming this would be defined elsewhere in your project)
class ApiClient:
    def __init__(self):
        print("ApiClient initialized")
        self._closed = False

    def get(self, endpoint):
        if self._closed:
            raise RuntimeError("API client is closed")
        print(f"GET request to {endpoint}")
        # Simulate an API response
        if endpoint == "/endpoint":
            return MockResponse({"data": "sample_data"}, 200)
        return MockResponse({}, 404)

    def close(self):
        print("ApiClient closed")
        self._closed = True

# Example MockResponse class (to simulate API responses)
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

# conftest.py content example
@pytest.fixture(scope="session")
def api_client():
    """Session-scoped fixture for an API client."""
    client = ApiClient()
    yield client  # Provide the client to the test
    client.close() # Teardown: close the client after all tests in the session are done

# test_api.py content example

# This test function uses the `api_client` fixture defined above (or in conftest.py)
def test_api_request(api_client: ApiClient):
    """Test making a successful API request using the client fixture."""
    response = api_client.get("/endpoint")
    assert response.status_code == 200
    assert response.json() == {"data": "sample_data"}

# Example of a module-scoped fixture
@pytest.fixture(scope="module")
def db_connection():
    """Module-scoped fixture for a database connection (example)."""
    print("Setting up DB connection (module scope)")
    conn = object() # Replace with actual DB connection setup
    yield conn
    print("Tearing down DB connection (module scope)")
    # Add cleanup code for the DB connection if needed

def test_something_with_db(db_connection):
    """Test function using the module-scoped database connection."""
    assert db_connection is not None
    # Perform tests that require db_connection
    print("Test executed with DB connection") 