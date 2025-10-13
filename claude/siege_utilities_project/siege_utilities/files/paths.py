"""
Path manipulation utilities for siege_utilities.
Provides functions for working with file paths and archives.
"""

import zipfile
import logging
import shutil
import re
from pathlib import Path
from typing import Union, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

FilePath = Union[str, Path]


def ensure_path_exists(path: FilePath, create_gitkeep: bool = True) -> Path:
    """
    Ensure a directory path exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists
        create_gitkeep: Whether to create .gitkeep file in new directories

    Returns:
        Path object for the directory

    Example:
        >>> data_dir = ensure_path_exists('data/processed')
        >>> print(f"Directory ready: {data_dir}")
    """
    try:
        path_obj = Path(path)

        # Create directory if it doesn't exist
        if not path_obj.exists():
            path_obj.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path_obj}")

            # Create .gitkeep to track empty directories in git
            if create_gitkeep:
                gitkeep = path_obj / '.gitkeep'
                gitkeep.touch()
                logger.debug(f"Created .gitkeep in {path_obj}")

        return path_obj

    except Exception as e:
        logger.error(f"Failed to ensure path exists {path}: {e}")
        raise


def unzip_file_to_directory(zip_path: FilePath,
                            extract_to: Optional[FilePath] = None,
                            remove_zip: bool = False) -> Optional[Path]:
    """
    Extract a ZIP file to a directory.

    Args:
        zip_path: Path to ZIP file
        extract_to: Directory to extract to (defaults to zip file's parent with zip name)
        remove_zip: Whether to remove ZIP file after extraction

    Returns:
        Path to extraction directory, or None if failed

    Example:
        >>> extracted = unzip_file_to_directory('data.zip')
        >>> print(f"Extracted to: {extracted}")
    """
    try:
        zip_path_obj = Path(zip_path)

        if not zip_path_obj.exists():
            logger.error(f"ZIP file does not exist: {zip_path_obj}")
            return None

        # Check if it's a valid ZIP file
        if not zipfile.is_zipfile(zip_path_obj):
            logger.error(f"Not a valid ZIP file: {zip_path_obj}")
            return None

        # Determine extraction directory
        if extract_to is None:
            # Extract to directory named after zip file (without extension)
            extract_to = zip_path_obj.parent / zip_path_obj.stem

        extract_path = Path(extract_to)
        extract_path.mkdir(parents=True, exist_ok=True)

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path_obj, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        logger.info(f"Extracted {zip_path_obj} to {extract_path}")

        # Optionally remove the ZIP file
        if remove_zip:
            zip_path_obj.unlink()
            logger.info(f"Removed ZIP file: {zip_path_obj}")

        return extract_path

    except zipfile.BadZipFile:
        logger.error(f"Corrupt ZIP file: {zip_path}")
        return None
    except Exception as e:
        logger.error(f"Failed to extract ZIP file {zip_path}: {e}")
        return None


def get_file_extension(file_path: FilePath, include_dot: bool = True) -> str:
    """
    Get file extension from path.

    Args:
        file_path: Path to file
        include_dot: Whether to include the dot in extension

    Returns:
        File extension

    Example:
        >>> ext = get_file_extension('document.pdf')
        >>> print(ext)  # '.pdf'
    """
    path_obj = Path(file_path)
    extension = path_obj.suffix

    if not include_dot and extension.startswith('.'):
        extension = extension[1:]

    return extension


def get_file_name_without_extension(file_path: FilePath) -> str:
    """
    Get filename without extension.

    Args:
        file_path: Path to file

    Returns:
        Filename without extension

    Example:
        >>> name = get_file_name_without_extension('data/report.pdf')
        >>> print(name)  # 'report'
    """
    path_obj = Path(file_path)
    return path_obj.stem


def is_hidden_file(file_path: FilePath) -> bool:
    """
    Check if file is hidden (starts with dot on Unix).

    Args:
        file_path: Path to file

    Returns:
        True if hidden, False otherwise

    Example:
        >>> if is_hidden_file('.gitignore'):
        ...     print("This is a hidden file")
    """
    path_obj = Path(file_path)
    return path_obj.name.startswith('.')


def normalize_path(path: FilePath, resolve: bool = True) -> Path:
    """
    Normalize a file path (expand user, resolve symlinks, etc.).

    Args:
        path: Path to normalize
        resolve: Whether to resolve symlinks and make absolute

    Returns:
        Normalized Path object

    Example:
        >>> norm_path = normalize_path('~/data/../files')
        >>> print(norm_path)
    """
    path_obj = Path(path).expanduser()

    if resolve:
        path_obj = path_obj.resolve()

    return path_obj


def get_relative_path(path: FilePath, base: FilePath) -> Path:
    """
    Get relative path from base to target path.

    Args:
        path: Target path
        base: Base path

    Returns:
        Relative path

    Example:
        >>> rel = get_relative_path('/home/user/data/file.csv', '/home/user')
        >>> print(rel)  # 'data/file.csv'
    """
    try:
        path_obj = Path(path).resolve()
        base_obj = Path(base).resolve()
        return path_obj.relative_to(base_obj)
    except ValueError:
        logger.warning(f"Cannot create relative path from {base} to {path}")
        return Path(path)


def create_backup_path(file_path: FilePath, suffix: Optional[str] = None) -> Path:
    """
    Create a backup path for a file.

    Args:
        file_path: Original file path
        suffix: Suffix to add (defaults to timestamp)

    Returns:
        Backup file path

    Example:
        >>> backup = create_backup_path('config.yaml')
        >>> print(backup)  # 'config.yaml.bak_20231012_143022'
    """
    path_obj = Path(file_path)

    if suffix is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        suffix = f"bak_{timestamp}"

    backup_path = path_obj.parent / f"{path_obj.name}.{suffix}"
    return backup_path


def find_files_by_pattern(directory: FilePath,
                          pattern: str = '*',
                          recursive: bool = True) -> List[Path]:
    """
    Find files matching a glob pattern in a directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern (e.g., '*.csv', '**/*.py')
        recursive: Whether to search recursively

    Returns:
        List of matching file paths

    Example:
        >>> csv_files = find_files_by_pattern('data', '*.csv')
        >>> py_files = find_files_by_pattern('src', '**/*.py', recursive=True)
    """
    try:
        dir_path = Path(directory)

        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Directory does not exist: {dir_path}")
            return []

        if recursive:
            matches = list(dir_path.rglob(pattern))
        else:
            matches = list(dir_path.glob(pattern))

        # Filter to only files (not directories)
        files = [p for p in matches if p.is_file()]

        logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
        return sorted(files)

    except Exception as e:
        logger.error(f"Failed to find files in {directory}: {e}")
        return []


def sanitize_filename(filename: str, replacement: str = '_') -> str:
    """
    Sanitize filename by removing/replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid chars with

    Returns:
        Sanitized filename

    Example:
        >>> safe_name = sanitize_filename('report: Q4 2023.pdf')
        >>> print(safe_name)  # 'report_ Q4 2023.pdf'
    """
    # Remove/replace characters that are invalid in filenames
    # Invalid: \ / : * ? " < > |
    invalid_chars = r'[\\/:*?"<>|]'
    sanitized = re.sub(invalid_chars, replacement, filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')

    return sanitized


def get_directory_size(directory: FilePath) -> int:
    """
    Calculate total size of all files in a directory.

    Args:
        directory: Directory path

    Returns:
        Total size in bytes

    Example:
        >>> size = get_directory_size('data')
        >>> print(f"Directory size: {size / (1024**2):.2f} MB")
    """
    try:
        dir_path = Path(directory)

        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Directory does not exist: {dir_path}")
            return 0

        total_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())

        logger.debug(f"Directory size for {dir_path}: {total_size} bytes")
        return total_size

    except Exception as e:
        logger.error(f"Failed to calculate directory size for {directory}: {e}")
        return 0


def copy_directory_tree(source: FilePath,
                       destination: FilePath,
                       ignore_patterns: Optional[List[str]] = None) -> bool:
    """
    Copy entire directory tree from source to destination.

    Args:
        source: Source directory
        destination: Destination directory
        ignore_patterns: List of patterns to ignore (e.g., ['*.pyc', '__pycache__'])

    Returns:
        True if successful, False otherwise

    Example:
        >>> copy_directory_tree('src', 'backup/src', ignore_patterns=['*.pyc'])
    """
    try:
        source_path = Path(source)
        dest_path = Path(destination)

        if not source_path.exists():
            logger.error(f"Source directory does not exist: {source_path}")
            return False

        # Create ignore function if patterns provided
        ignore_func = None
        if ignore_patterns:
            ignore_func = shutil.ignore_patterns(*ignore_patterns)

        shutil.copytree(source_path, dest_path, ignore=ignore_func, dirs_exist_ok=True)

        logger.info(f"Copied directory tree from {source_path} to {dest_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to copy directory tree: {e}")
        return False


__all__ = [
    'ensure_path_exists',
    'unzip_file_to_directory',
    'get_file_extension',
    'get_file_name_without_extension',
    'is_hidden_file',
    'normalize_path',
    'get_relative_path',
    'create_backup_path',
    'find_files_by_pattern',
    'sanitize_filename',
    'get_directory_size',
    'copy_directory_tree'
]
