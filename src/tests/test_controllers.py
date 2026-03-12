import pytest
from src.presentation.controllers.chat.send_message import SendMessageController
from src.presentation.http_types.http_request import HttpRequest


class TestSendMessageController:
    """Test SendMessageController."""

    @pytest.mark.asyncio
    async def test_handle_success(self, mock_chat_ai_use_case):
        """Test successful message handling."""
        controller = SendMessageController(chat_ai_use_case=mock_chat_ai_use_case)
        
        http_request = HttpRequest(
            body={"content": "Hello AI"},
            header={},
            path_params={},
            query_params={}
        )
        
        response = await controller.handle(http_request)
        
        assert response.data == "Test AI response"
        mock_chat_ai_use_case.send_message.assert_called_once_with(message="Hello AI")

    @pytest.mark.asyncio
    async def test_handle_empty_body(self, mock_chat_ai_use_case):
        """Test handling request with no body."""
        controller = SendMessageController(chat_ai_use_case=mock_chat_ai_use_case)
        
        http_request = HttpRequest(
            body=None,
            header={},
            path_params={},
            query_params={}
        )
        
        response = await controller.handle(http_request)
        
        assert response.data == "Test AI response"
        mock_chat_ai_use_case.send_message.assert_called_once_with(message="")

    @pytest.mark.asyncio
    async def test_handle_missing_content_field(self, mock_chat_ai_use_case):
        """Test handling request with body but no content field."""
        controller = SendMessageController(chat_ai_use_case=mock_chat_ai_use_case)
        
        http_request = HttpRequest(
            body={"other_field": "value"},
            header={},
            path_params={},
            query_params={}
        )
        
        response = await controller.handle(http_request)
        
        assert response.data == "Test AI response"
        mock_chat_ai_use_case.send_message.assert_called_once_with(message="")

    @pytest.mark.asyncio
    async def test_handle_use_case_error(self, mock_chat_ai_use_case):
        """Test handling use case errors."""
        mock_chat_ai_use_case.send_message.side_effect = Exception("Use case error")
        controller = SendMessageController(chat_ai_use_case=mock_chat_ai_use_case)
        
        http_request = HttpRequest(
            body={"content": "Hello"},
            header={},
            path_params={},
            query_params={}
        )
        
        with pytest.raises(Exception, match="Use case error"):
            await controller.handle(http_request)

    @pytest.mark.asyncio
    async def test_handle_with_empty_content(self, mock_chat_ai_use_case):
        """Test handling request with empty content."""
        controller = SendMessageController(chat_ai_use_case=mock_chat_ai_use_case)
        
        http_request = HttpRequest(
            body={"content": ""},
            header={},
            path_params={},
            query_params={}
        )
        
        response = await controller.handle(http_request)
        
        assert response.data == "Test AI response"
        mock_chat_ai_use_case.send_message.assert_called_once_with(message="")
