"""
HDFS operations utilities for siege_utilities.

**IMPORTANT: These functions are NOT IMPLEMENTED.**
They are placeholder stubs that return None/False and log warnings.

To use HDFS operations, you will need to:
1. Install PyArrow (`pip install pyarrow`) or HDFS3 (`pip install hdfs3`)
2. Implement actual HDFS connection and operations
3. These functions currently do not connect to any HDFS cluster

**Production Status:** NOT PRODUCTION READY - Stubs only
"""

import logging
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


def hdfs_list_directory(path: str, config: Optional[dict] = None) -> Optional[List[str]]:
    """
    List files in HDFS directory.

    **WARNING: NOT IMPLEMENTED - This is a stub function that always returns None.**

    Args:
        path: HDFS path
        config: HDFS configuration

    Returns:
        Always returns None (not implemented)

    Raises:
        NotImplementedError: If you attempt to use this in production
    """
    logger.error("hdfs_list_directory is NOT IMPLEMENTED. This is a stub function.")
    logger.warning("HDFS operations require PyArrow or HDFS3 library and actual implementation")
    raise NotImplementedError(
        "HDFS operations are not implemented. "
        "This is a placeholder stub. "
        "To use HDFS, install pyarrow and implement actual HDFS connection logic."
    )


def hdfs_upload_file(local_path: Path, hdfs_path: str, config: Optional[dict] = None) -> bool:
    """
    Upload file to HDFS.

    **WARNING: NOT IMPLEMENTED - This is a stub function that always raises NotImplementedError.**

    Args:
        local_path: Local file path
        hdfs_path: HDFS destination path
        config: HDFS configuration

    Returns:
        Never returns (raises exception)

    Raises:
        NotImplementedError: Always raised
    """
    logger.error("hdfs_upload_file is NOT IMPLEMENTED. This is a stub function.")
    raise NotImplementedError(
        "HDFS operations are not implemented. "
        "This is a placeholder stub. "
        "To use HDFS, install pyarrow and implement actual HDFS connection logic."
    )


def hdfs_download_file(hdfs_path: str, local_path: Path, config: Optional[dict] = None) -> bool:
    """
    Download file from HDFS.

    **WARNING: NOT IMPLEMENTED - This is a stub function that always raises NotImplementedError.**

    Args:
        hdfs_path: HDFS source path
        local_path: Local destination path
        config: HDFS configuration

    Returns:
        Never returns (raises exception)

    Raises:
        NotImplementedError: Always raised
    """
    logger.error("hdfs_download_file is NOT IMPLEMENTED. This is a stub function.")
    raise NotImplementedError(
        "HDFS operations are not implemented. "
        "This is a placeholder stub. "
        "To use HDFS, install pyarrow and implement actual HDFS connection logic."
    )


def hdfs_delete_file(path: str, config: Optional[dict] = None) -> bool:
    """
    Delete file from HDFS.

    **WARNING: NOT IMPLEMENTED - This is a stub function that always raises NotImplementedError.**

    Args:
        path: HDFS file path
        config: HDFS configuration

    Returns:
        Never returns (raises exception)

    Raises:
        NotImplementedError: Always raised
    """
    logger.error("hdfs_delete_file is NOT IMPLEMENTED. This is a stub function.")
    raise NotImplementedError(
        "HDFS operations are not implemented. "
        "This is a placeholder stub. "
        "To use HDFS, install pyarrow and implement actual HDFS connection logic."
    )


__all__ = [
    'hdfs_list_directory',
    'hdfs_upload_file',
    'hdfs_download_file',
    'hdfs_delete_file'
]
