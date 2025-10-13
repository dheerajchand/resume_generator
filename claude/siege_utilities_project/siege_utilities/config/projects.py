"""
Project configuration management for siege_utilities.
Provides utilities for managing project-level configurations.
"""

import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


def create_project_config(project_name: str,
                         project_root: Path,
                         description: str = '',
                         **kwargs) -> Dict[str, Any]:
    """
    Create a project configuration dictionary.

    Args:
        project_name: Name of the project
        project_root: Root directory for the project
        description: Project description
        **kwargs: Additional configuration options

    Returns:
        Project configuration dictionary
    """
    config = {
        'project_name': project_name,
        'project_root': str(project_root),
        'description': description,
        'created_at': datetime.now().isoformat(),
        'data_dir': str(project_root / 'data'),
        'output_dir': str(project_root / 'output'),
        'config_dir': str(project_root / 'config'),
        'logs_dir': str(project_root / 'logs')
    }
    config.update(kwargs)
    return config


def save_project_config(config: Dict[str, Any],
                       config_dir: Optional[Path] = None) -> bool:
    """
    Save project configuration to file.

    Args:
        config: Project configuration dictionary
        config_dir: Configuration directory

    Returns:
        True if successful
    """
    try:
        if config_dir is None:
            config_dir = Path.home() / '.siege_utilities' / 'projects'

        config_dir.mkdir(parents=True, exist_ok=True)
        project_name = config.get('project_name', 'default')
        config_file = config_dir / f'{project_name}.yaml'

        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        logger.info(f"Saved project config: {config_file}")
        return True

    except Exception as e:
        logger.error(f"Failed to save project config: {e}")
        return False


def load_project_config(project_name: str,
                       config_dir: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Load project configuration from file.

    Args:
        project_name: Name of the project
        config_dir: Configuration directory

    Returns:
        Project configuration dictionary or None
    """
    try:
        if config_dir is None:
            config_dir = Path.home() / '.siege_utilities' / 'projects'

        config_file = config_dir / f'{project_name}.yaml'

        if not config_file.exists():
            logger.warning(f"Project config not found: {config_file}")
            return None

        with open(config_file) as f:
            config = yaml.safe_load(f)

        logger.info(f"Loaded project config: {project_name}")
        return config

    except Exception as e:
        logger.error(f"Failed to load project config: {e}")
        return None


def setup_project_directories(project_root: Path,
                              directories: Optional[List[str]] = None) -> bool:
    """
    Create standard project directory structure.

    Args:
        project_root: Root directory for project
        directories: List of directory names to create

    Returns:
        True if successful
    """
    try:
        if directories is None:
            directories = ['data', 'output', 'config', 'logs', 'notebooks', 'scripts']

        project_root = Path(project_root)
        project_root.mkdir(parents=True, exist_ok=True)

        for dir_name in directories:
            (project_root / dir_name).mkdir(exist_ok=True)

        logger.info(f"Created project directories in {project_root}")
        return True

    except Exception as e:
        logger.error(f"Failed to setup project directories: {e}")
        return False


def get_project_path(project_name: str,
                    subdir: Optional[str] = None,
                    config_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Get path to project or project subdirectory.

    Args:
        project_name: Name of the project
        subdir: Subdirectory name (e.g., 'data', 'output')
        config_dir: Configuration directory

    Returns:
        Path to project or subdirectory
    """
    config = load_project_config(project_name, config_dir)

    if config is None:
        return None

    project_root = Path(config['project_root'])

    if subdir is None:
        return project_root

    return project_root / subdir


def list_projects(config_dir: Optional[Path] = None) -> List[str]:
    """
    List all configured projects.

    Args:
        config_dir: Configuration directory

    Returns:
        List of project names
    """
    try:
        if config_dir is None:
            config_dir = Path.home() / '.siege_utilities' / 'projects'

        if not config_dir.exists():
            return []

        project_files = config_dir.glob('*.yaml')
        projects = [f.stem for f in project_files]

        return sorted(projects)

    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        return []


def update_project_config(project_name: str,
                         updates: Dict[str, Any],
                         config_dir: Optional[Path] = None) -> bool:
    """
    Update project configuration.

    Args:
        project_name: Name of the project
        updates: Dictionary of updates to apply
        config_dir: Configuration directory

    Returns:
        True if successful
    """
    try:
        config = load_project_config(project_name, config_dir)

        if config is None:
            logger.error(f"Project config not found: {project_name}")
            return False

        config.update(updates)
        config['updated_at'] = datetime.now().isoformat()

        return save_project_config(config, config_dir)

    except Exception as e:
        logger.error(f"Failed to update project config: {e}")
        return False


__all__ = [
    'create_project_config',
    'save_project_config',
    'load_project_config',
    'setup_project_directories',
    'get_project_path',
    'list_projects',
    'update_project_config'
]
