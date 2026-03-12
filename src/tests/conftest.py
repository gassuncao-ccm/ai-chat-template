"""Pytest configuration and shared fixtures."""
import pytest
from unittest.mock import AsyncMock

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def mock_ai_strategy():
    """Mock AI strategy for testing."""
    strategy = AsyncMock()
    strategy.generate_response = AsyncMock(return_value="Mocked AI response")
    return strategy


@pytest.fixture
def mock_chat_ai_use_case():
    """Mock ChatAI use case for testing."""
    use_case = AsyncMock()
    use_case.send_message = AsyncMock(return_value="Test AI response")
    return use_case


@pytest.fixture
def sample_http_request():
    """Sample HTTP request for testing."""
    from src.presentation.http_types.http_request import HttpRequest
    return HttpRequest(
        body={"content": "test message"},
        header={},
        path_params={},
        query_params={}
    )
