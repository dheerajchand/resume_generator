"""
File hashing utilities for siege_utilities.
Provides functions to calculate and verify file hashes.
"""

import hashlib
import logging
from pathlib import Path
from typing import Union, Optional, Dict

logger = logging.getLogger(__name__)

FilePath = Union[str, Path]


def calculate_file_hash(file_path: FilePath, algorithm: str = 'sha256') -> Optional[str]:
    """
    Calculate hash of a file using specified algorithm.

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)

    Returns:
        Hash string or None if failed

    Example:
        >>> hash_val = calculate_file_hash('data.csv')
        >>> print(f"SHA256: {hash_val}")
    """
    try:
        path_obj = Path(file_path)

        if not path_obj.exists():
            logger.error(f"File does not exist: {path_obj}")
            return None

        if not path_obj.is_file():
            logger.error(f"Path is not a file: {path_obj}")
            return None

        # Get hash function
        if algorithm not in hashlib.algorithms_available:
            logger.error(f"Unsupported hash algorithm: {algorithm}")
            return None

        hash_func = hashlib.new(algorithm)

        # Read file in chunks to handle large files
        with open(path_obj, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_func.update(chunk)

        hash_value = hash_func.hexdigest()
        logger.debug(f"Calculated {algorithm} hash for {path_obj}: {hash_value}")
        return hash_value

    except Exception as e:
        logger.error(f"Failed to calculate hash for {file_path}: {e}")
        return None


def generate_sha256_hash_for_file(file_path: FilePath) -> Optional[str]:
    """
    Generate SHA256 hash for a file.

    Args:
        file_path: Path to file

    Returns:
        SHA256 hash string or None if failed

    Example:
        >>> hash_val = generate_sha256_hash_for_file('document.pdf')
    """
    return calculate_file_hash(file_path, algorithm='sha256')


def get_file_hash(file_path: FilePath, algorithm: str = 'md5') -> Optional[str]:
    """
    Get hash of a file (alias for calculate_file_hash).

    Args:
        file_path: Path to file
        algorithm: Hash algorithm

    Returns:
        Hash string or None if failed
    """
    return calculate_file_hash(file_path, algorithm)


def get_quick_file_signature(file_path: FilePath, sample_size: int = 8192) -> Optional[str]:
    """
    Generate quick file signature by hashing first N bytes.
    Useful for fast comparison of large files.

    Args:
        file_path: Path to file
        sample_size: Number of bytes to sample

    Returns:
        MD5 hash of sample or None if failed

    Example:
        >>> sig = get_quick_file_signature('large_file.bin')
    """
    try:
        path_obj = Path(file_path)

        if not path_obj.exists():
            logger.error(f"File does not exist: {path_obj}")
            return None

        hash_func = hashlib.md5()

        with open(path_obj, 'rb') as f:
            sample = f.read(sample_size)
            hash_func.update(sample)

        signature = hash_func.hexdigest()
        logger.debug(f"Quick signature for {path_obj}: {signature}")
        return signature

    except Exception as e:
        logger.error(f"Failed to generate signature for {file_path}: {e}")
        return None


def verify_file_integrity(file_path: FilePath,
                         expected_hash: str,
                         algorithm: str = 'sha256') -> bool:
    """
    Verify file integrity by comparing hash against expected value.

    Args:
        file_path: Path to file
        expected_hash: Expected hash value
        algorithm: Hash algorithm to use

    Returns:
        True if hash matches, False otherwise

    Example:
        >>> is_valid = verify_file_integrity('download.zip', 'abc123...', 'sha256')
        >>> if is_valid:
        ...     print("File integrity verified")
    """
    try:
        actual_hash = calculate_file_hash(file_path, algorithm)

        if actual_hash is None:
            logger.error(f"Could not calculate hash for {file_path}")
            return False

        # Case-insensitive comparison
        matches = actual_hash.lower() == expected_hash.lower()

        if matches:
            logger.info(f"File integrity verified: {file_path}")
        else:
            logger.warning(f"Hash mismatch for {file_path}")
            logger.warning(f"Expected: {expected_hash}")
            logger.warning(f"Actual: {actual_hash}")

        return matches

    except Exception as e:
        logger.error(f"Failed to verify integrity for {file_path}: {e}")
        return False


def generate_checksums_for_directory(directory: FilePath,
                                     algorithm: str = 'sha256',
                                     pattern: str = '*') -> Dict[str, str]:
    """
    Generate checksums for all files in a directory.

    Args:
        directory: Directory path
        algorithm: Hash algorithm
        pattern: Glob pattern for file matching

    Returns:
        Dictionary mapping file paths to hash values

    Example:
        >>> checksums = generate_checksums_for_directory('data/', pattern='*.csv')
    """
    try:
        dir_path = Path(directory)

        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Directory does not exist: {dir_path}")
            return {}

        checksums = {}

        for file_path in dir_path.rglob(pattern):
            if file_path.is_file():
                hash_val = calculate_file_hash(file_path, algorithm)
                if hash_val:
                    # Store relative path as key
                    rel_path = file_path.relative_to(dir_path)
                    checksums[str(rel_path)] = hash_val

        logger.info(f"Generated checksums for {len(checksums)} files in {dir_path}")
        return checksums

    except Exception as e:
        logger.error(f"Failed to generate checksums for directory {directory}: {e}")
        return {}


__all__ = [
    'calculate_file_hash',
    'generate_sha256_hash_for_file',
    'get_file_hash',
    'get_quick_file_signature',
    'verify_file_integrity',
    'generate_checksums_for_directory'
]
