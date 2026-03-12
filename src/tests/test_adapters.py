import pytest
from unittest.mock import AsyncMock, MagicMock
from src.main.adapters.request_adapter import request_adapter
from src.presentation.http_types.http_response import SuccessResponse


class TestRequestAdapter:
    """Test request adapter."""

    @pytest.mark.asyncio
    async def test_request_adapter_success(self):
        """Test successful request adaptation."""
        mock_request = MagicMock()
        mock_request.headers = {"Content-Type": "application/json"}
        mock_request.query_params = {}
        mock_request.json = AsyncMock(return_value={})
        
        mock_controller = AsyncMock()
        mock_controller.return_value = SuccessResponse(data="Success")
        
        response = await request_adapter(mock_request, mock_controller)
        
        assert response.data == "Success"
        mock_controller.assert_called_once()

    @pytest.mark.asyncio
    async def test_request_adapter_passes_correct_http_request(self):
        """Test that adapter creates correct HttpRequest."""
        mock_request = MagicMock()
        mock_request.headers = {"Authorization": "Bearer token"}
        mock_request.query_params = {"filter": "active"}
        mock_request.json = AsyncMock(return_value={"test": "data"})
        mock_request.url = "http://test.com"
        
        captured_http_request = None
        
        async def capture_controller(http_request):
            nonlocal captured_http_request
            captured_http_request = http_request
            return SuccessResponse(data="OK")
        
        await request_adapter(mock_request, capture_controller, path_params={"id": "123"})
        
        # Verify the HttpRequest was created with correct data
        assert captured_http_request is not None
        assert captured_http_request.header == {"Authorization": "Bearer token"}
        assert captured_http_request.path_params == {"id": "123"}
        assert captured_http_request.query_params == {"filter": "active"}
        assert captured_http_request.body == {"test": "data"}
