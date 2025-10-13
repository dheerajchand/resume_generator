"""
String utility functions for siege_utilities.
Provides text manipulation and cleaning utilities.
"""

import re
from typing import Optional


def remove_wrapping_quotes_and_trim(text: str) -> str:
    """
    Remove wrapping quotes (single or double) and trim whitespace.

    Args:
        text: Input string potentially wrapped in quotes

    Returns:
        Cleaned string with quotes and whitespace removed

    Example:
        >>> remove_wrapping_quotes_and_trim('"hello world"')
        'hello world'
        >>> remove_wrapping_quotes_and_trim("  'test'  ")
        'test'
    """
    if not isinstance(text, str):
        return str(text)

    # Trim whitespace first
    text = text.strip()

    # Remove wrapping quotes
    if len(text) >= 2:
        if (text[0] == '"' and text[-1] == '"') or (text[0] == "'" and text[-1] == "'"):
            text = text[1:-1]

    # Final trim
    return text.strip()


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace by replacing multiple spaces with single space.

    Args:
        text: Input string

    Returns:
        String with normalized whitespace
    """
    return re.sub(r'\s+', ' ', text).strip()


def remove_special_characters(text: str, keep: str = '') -> str:
    """
    Remove special characters from string, optionally keeping specified ones.

    Args:
        text: Input string
        keep: Characters to keep (e.g., '-_')

    Returns:
        String with special characters removed
    """
    pattern = f'[^a-zA-Z0-9{re.escape(keep)}]'
    return re.sub(pattern, '', text)


def truncate_string(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate string to maximum length, adding suffix if truncated.

    Args:
        text: Input string
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def camel_to_snake(text: str) -> str:
    """
    Convert camelCase to snake_case.

    Args:
        text: CamelCase string

    Returns:
        snake_case string
    """
    text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', text).lower()


def snake_to_camel(text: str) -> str:
    """
    Convert snake_case to camelCase.

    Args:
        text: snake_case string

    Returns:
        camelCase string
    """
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


__all__ = [
    'remove_wrapping_quotes_and_trim',
    'normalize_whitespace',
    'remove_special_characters',
    'truncate_string',
    'camel_to_snake',
    'snake_to_camel'
]
