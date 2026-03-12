from src.infrastructure.config.settings import Settings


class TestSettings:
    """Test application settings."""

    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()
        
        assert settings.APP_NAME == "DEFAULT APP NAME"
        assert settings.APP_PORT == 8999
        assert settings.APP_VERSION == "0.1.0"
        assert settings.CONVERSATION_MODEL == "gpt-4.1"

    def test_settings_override(self, monkeypatch):
        """Test settings can be overridden by environment variables."""
        monkeypatch.setenv("APP_NAME", "Test App")
        monkeypatch.setenv("APP_PORT", "9000")
        monkeypatch.setenv("APP_VERSION", "1.0.0")
        monkeypatch.setenv("CONVERSATION_MODEL", "gpt-4o")
        
        settings = Settings()
        
        assert settings.APP_NAME == "Test App"
        assert settings.APP_PORT == 9000
        assert settings.APP_VERSION == "1.0.0"
        assert settings.CONVERSATION_MODEL == "gpt-4o"

    def test_settings_partial_override(self, monkeypatch):
        """Test partial settings override."""
        monkeypatch.setenv("APP_NAME", "Custom Name")
        
        settings = Settings()
        
        assert settings.APP_NAME == "Custom Name"
        assert settings.APP_PORT == 8999
        assert settings.APP_VERSION == "0.1.0"
