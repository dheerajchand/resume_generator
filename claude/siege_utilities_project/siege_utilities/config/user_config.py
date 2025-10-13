"""
User configuration management for siege_utilities.
Legacy module - redirects to enhanced_config for backward compatibility.
"""

# Re-export everything from enhanced_config
from .enhanced_config import (
    UserProfile,
    SiegeConfig,
    load_user_profile,
    save_user_profile,
    get_download_directory,
    list_client_profiles
)


class UserConfigManager:
    """
    Legacy UserConfigManager class for backward compatibility.
    Wraps SiegeConfig functionality.
    """

    def __init__(self, config_dir=None):
        self.config = SiegeConfig(config_dir)

    def get_user_profile(self, username: str):
        """Get user profile."""
        return self.config.get_user_profile(username)

    def save_user_profile(self, profile, username: str):
        """Save user profile."""
        return self.config.save_user_profile(profile, username)

    def get_download_directory(self, username: str):
        """Get download directory for user."""
        return get_download_directory(username)


# Singleton instance for backward compatibility
user_config = UserConfigManager()


def get_user_config():
    """Get the global user config manager instance."""
    return user_config


__all__ = [
    'UserProfile',
    'UserConfigManager',
    'SiegeConfig',
    'user_config',
    'get_user_config',
    'get_download_directory',
    'load_user_profile',
    'save_user_profile',
    'list_client_profiles'
]
