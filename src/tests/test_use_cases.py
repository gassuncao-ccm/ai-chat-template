import pytest
from unittest.mock import AsyncMock
from src.application.use_cases.chat_ai import ChatAI


class TestChatAI:
    """Test ChatAI use case."""

    @pytest.mark.asyncio
    async def test_send_message_success(self, mock_ai_strategy):
        """Test successful message sending."""
        use_case = ChatAI(ai_strategy=mock_ai_strategy)
        
        result = await use_case.send_message(message="Hello")
        
        assert result == "Mocked AI response"
        mock_ai_strategy.generate_response.assert_called_once_with("Hello")

    @pytest.mark.asyncio
    async def test_send_message_with_empty_string(self, mock_ai_strategy):
        """Test sending empty message."""
        use_case = ChatAI(ai_strategy=mock_ai_strategy)
        
        result = await use_case.send_message(message="")
        
        assert result == "Mocked AI response"
        mock_ai_strategy.generate_response.assert_called_once_with("")

    @pytest.mark.asyncio
    async def test_send_message_strategy_error(self, mock_ai_strategy):
        """Test handling strategy errors."""
        mock_ai_strategy.generate_response = AsyncMock(
            side_effect=Exception("AI Error")
        )
        use_case = ChatAI(ai_strategy=mock_ai_strategy)
        
        with pytest.raises(Exception, match="AI Error"):
            await use_case.send_message(message="Hello")

    @pytest.mark.asyncio
    async def test_send_message_multiple_calls(self, mock_ai_strategy):
        """Test multiple message calls."""
        mock_ai_strategy.generate_response = AsyncMock(
            side_effect=["Response 1", "Response 2", "Response 3"]
        )
        use_case = ChatAI(ai_strategy=mock_ai_strategy)
        
        result1 = await use_case.send_message(message="Message 1")
        result2 = await use_case.send_message(message="Message 2")
        result3 = await use_case.send_message(message="Message 3")
        
        assert result1 == "Response 1"
        assert result2 == "Response 2"
        assert result3 == "Response 3"
        assert mock_ai_strategy.generate_response.call_count == 3
