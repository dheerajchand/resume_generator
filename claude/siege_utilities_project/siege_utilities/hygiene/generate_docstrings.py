"""
Docstring generation utilities for siege_utilities.
Provides tools to generate and analyze function docstrings.
"""

import ast
import inspect
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FunctionInfo:
    """Information about a function."""
    name: str
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    line_number: int
    category: str


def analyze_function_signature(func) -> Dict[str, Any]:
    """
    Analyze function signature to extract parameter and return information.

    Args:
        func: Function object to analyze

    Returns:
        Dictionary containing function signature information
    """
    try:
        sig = inspect.signature(func)

        info = {
            'name': func.__name__,
            'parameters': [],
            'return_annotation': None,
            'docstring': inspect.getdoc(func)
        }

        for param_name, param in sig.parameters.items():
            param_info = {
                'name': param_name,
                'annotation': str(param.annotation) if param.annotation != inspect.Parameter.empty else None,
                'default': str(param.default) if param.default != inspect.Parameter.empty else None
            }
            info['parameters'].append(param_info)

        if sig.return_annotation != inspect.Signature.empty:
            info['return_annotation'] = str(sig.return_annotation)

        return info

    except Exception as e:
        logger.error(f"Failed to analyze function signature: {e}")
        return {}


def categorize_function(func_name: str, module_name: str = '') -> str:
    """
    Categorize a function based on its name and module.

    Args:
        func_name: Name of the function
        module_name: Module containing the function

    Returns:
        Category string
    """
    # Simple categorization based on naming patterns
    categories = {
        'get_': 'accessor',
        'set_': 'mutator',
        'create_': 'constructor',
        'load_': 'io',
        'save_': 'io',
        'read_': 'io',
        'write_': 'io',
        'download_': 'io',
        'upload_': 'io',
        'calculate_': 'computation',
        'compute_': 'computation',
        'validate_': 'validation',
        'check_': 'validation',
        'verify_': 'validation',
        'generate_': 'generator',
        'parse_': 'parser',
        'format_': 'formatter',
        'convert_': 'converter',
        'transform_': 'transformer'
    }

    for prefix, category in categories.items():
        if func_name.startswith(prefix):
            return category

    return 'utility'


def generate_docstring_template(func_name: str,
                                params: List[Dict[str, Any]],
                                return_type: Optional[str] = None,
                                category: str = 'utility') -> str:
    """
    Generate a docstring template for a function.

    Args:
        func_name: Name of the function
        params: List of parameter dictionaries
        return_type: Return type annotation
        category: Function category

    Returns:
        Docstring template string

    Example:
        >>> template = generate_docstring_template('process_data',
        ...     [{'name': 'df', 'annotation': 'DataFrame'}],
        ...     'DataFrame')
    """
    lines = []

    # Brief description
    lines.append(f'"""')
    lines.append(f'{func_name.replace("_", " ").title()}.')
    lines.append('')

    # Args section
    if params:
        lines.append('Args:')
        for param in params:
            param_name = param['name']
            param_type = param.get('annotation', 'Any')
            param_default = param.get('default')

            if param_default:
                lines.append(f'    {param_name} ({param_type}, optional): Description. Defaults to {param_default}.')
            else:
                lines.append(f'    {param_name} ({param_type}): Description')
        lines.append('')

    # Returns section
    if return_type:
        lines.append('Returns:')
        lines.append(f'    {return_type}: Description')
        lines.append('')

    # Example section
    lines.append('Example:')
    lines.append(f'    >>> result = {func_name}(...)')

    lines.append('"""')

    return '\n'.join(lines)


def process_python_file(file_path: Path) -> List[FunctionInfo]:
    """
    Process a Python file to extract function information.

    Args:
        file_path: Path to Python file

    Returns:
        List of FunctionInfo objects
    """
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())

        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions
                if node.name.startswith('_'):
                    continue

                func_info = FunctionInfo(
                    name=node.name,
                    args=[arg.arg for arg in node.args.args],
                    returns=ast.unparse(node.returns) if node.returns else None,
                    docstring=ast.get_docstring(node),
                    line_number=node.lineno,
                    category=categorize_function(node.name)
                )

                functions.append(func_info)

        logger.info(f"Found {len(functions)} functions in {file_path}")
        return functions

    except Exception as e:
        logger.error(f"Failed to process file {file_path}: {e}")
        return []


def find_python_files(directory: Path, recursive: bool = True) -> List[Path]:
    """
    Find all Python files in a directory.

    Args:
        directory: Directory to search
        recursive: Whether to search recursively

    Returns:
        List of Python file paths
    """
    try:
        dir_path = Path(directory)

        if recursive:
            python_files = list(dir_path.rglob('*.py'))
        else:
            python_files = list(dir_path.glob('*.py'))

        # Filter out __pycache__ and other system files
        python_files = [
            f for f in python_files
            if '__pycache__' not in str(f) and not f.name.startswith('.')
        ]

        logger.info(f"Found {len(python_files)} Python files in {directory}")
        return sorted(python_files)

    except Exception as e:
        logger.error(f"Failed to find Python files: {e}")
        return []


def check_docstring_coverage(directory: Path) -> Dict[str, Any]:
    """
    Check docstring coverage for all functions in a directory.

    Args:
        directory: Directory to analyze

    Returns:
        Dictionary with coverage statistics
    """
    python_files = find_python_files(directory)

    total_functions = 0
    documented_functions = 0
    undocumented = []

    for file_path in python_files:
        functions = process_python_file(file_path)

        for func in functions:
            total_functions += 1
            if func.docstring:
                documented_functions += 1
            else:
                undocumented.append({
                    'file': str(file_path),
                    'function': func.name,
                    'line': func.line_number
                })

    coverage = (documented_functions / total_functions * 100) if total_functions > 0 else 0

    return {
        'total_functions': total_functions,
        'documented': documented_functions,
        'undocumented': len(undocumented),
        'coverage_percent': coverage,
        'undocumented_list': undocumented
    }


__all__ = [
    'FunctionInfo',
    'analyze_function_signature',
    'categorize_function',
    'generate_docstring_template',
    'process_python_file',
    'find_python_files',
    'check_docstring_coverage'
]
