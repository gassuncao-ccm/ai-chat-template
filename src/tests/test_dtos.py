from src.presentation.dtos.chat import SendMessageRequest


class TestSendMessageRequest:
    """Test SendMessageRequest DTO."""

    def test_valid_request_with_content(self):
        """Test creating a valid request with content."""
        request = SendMessageRequest(content="Hello AI")
        assert request.content == "Hello AI"

    def test_valid_request_without_content(self):
        """Test creating a valid request without content (optional field)."""
        request = SendMessageRequest()
        assert request.content is None

    def test_valid_request_with_none_content(self):
        """Test creating a valid request with None content."""
        request = SendMessageRequest(content=None)
        assert request.content is None

    def test_valid_request_with_empty_string(self):
        """Test creating a valid request with empty string."""
        request = SendMessageRequest(content="")
        assert request.content == ""

    def test_dict_conversion(self):
        """Test converting request to dict."""
        request = SendMessageRequest(content="test")
        data = request.model_dump()
        assert data == {"content": "test"}
