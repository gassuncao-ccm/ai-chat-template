from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import SuccessResponse


class TestHttpRequest:
    """Test HttpRequest type."""

    def test_create_request_with_all_fields(self):
        """Test creating request with all fields."""
        request = HttpRequest(
            body={"key": "value"},
            header={"Content-Type": "application/json"},
            path_params={"id": "123"},
            query_params={"filter": "active"}
        )
        
        assert request.body == {"key": "value"}
        assert request.header == {"Content-Type": "application/json"}
        assert request.path_params == {"id": "123"}
        assert request.query_params == {"filter": "active"}

    def test_create_request_with_empty_fields(self):
        """Test creating request with empty fields."""
        request = HttpRequest(
            body={},
            header={},
            path_params={},
            query_params={}
        )
        
        assert request.body == {}
        assert request.header == {}
        assert request.path_params == {}
        assert request.query_params == {}


class TestSuccessResponse:
    """Test SuccessResponse type."""

    def test_create_success_response_with_string(self):
        """Test creating success response with string data."""
        response = SuccessResponse(data="Success message")
        
        assert response.data == "Success message"
        assert response.success is True

    def test_create_success_response_with_dict(self):
        """Test creating success response with dict data."""
        response = SuccessResponse(data={"key": "value"})
        
        assert response.data == {"key": "value"}
        assert response.success is True

    def test_create_success_response_with_custom_success_flag(self):
        """Test creating success response with custom success flag."""
        response = SuccessResponse(data="Created", success=True)
        
        assert response.data == "Created"
        assert response.success is True

    def test_success_response_serialization(self):
        """Test success response can be serialized."""
        response = SuccessResponse(data="test")
        data = response.model_dump()
        
        assert "data" in data
        assert data["data"] == "test"
