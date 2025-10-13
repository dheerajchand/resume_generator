"""
HDFS configuration utilities for siege_utilities.
Provides configuration management for HDFS connections.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def create_hdfs_config(namenode: str,
                       port: int = 9000,
                       user: Optional[str] = None,
                       **kwargs) -> Dict[str, Any]:
    """
    Create HDFS configuration dictionary.

    Args:
        namenode: HDFS namenode hostname
        port: HDFS port
        user: HDFS user
        **kwargs: Additional configuration options

    Returns:
        Configuration dictionary
    """
    config = {
        'namenode': namenode,
        'port': port,
        'user': user or 'hdfs',
        'url': f'hdfs://{namenode}:{port}'
    }
    config.update(kwargs)
    return config


def load_hdfs_config(config_file: Path) -> Optional[Dict[str, Any]]:
    """
    Load HDFS configuration from file.

    Args:
        config_file: Path to configuration file

    Returns:
        Configuration dictionary or None
    """
    try:
        import yaml
        with open(config_file) as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load HDFS config: {e}")
        return None


def save_hdfs_config(config: Dict[str, Any], config_file: Path) -> bool:
    """
    Save HDFS configuration to file.

    Args:
        config: Configuration dictionary
        config_file: Path to save configuration

    Returns:
        True if successful
    """
    try:
        import yaml
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
        return True
    except Exception as e:
        logger.error(f"Failed to save HDFS config: {e}")
        return False


__all__ = [
    'create_hdfs_config',
    'load_hdfs_config',
    'save_hdfs_config'
]
