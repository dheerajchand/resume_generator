"""
Git branch analysis utilities for siege_utilities.
Provides tools to analyze git branch status and history.
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def get_git_root(path: Optional[Path] = None) -> Optional[Path]:
    """
    Get the root directory of the git repository.

    Args:
        path: Path within repository (defaults to current directory)

    Returns:
        Path to git root or None if not in a git repository
    """
    try:
        if path is None:
            path = Path.cwd()

        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )

        return Path(result.stdout.strip())

    except subprocess.CalledProcessError:
        logger.warning(f"Not a git repository: {path}")
        return None
    except Exception as e:
        logger.error(f"Failed to get git root: {e}")
        return None


def analyze_branch_status(branch_name: Optional[str] = None,
                         repo_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Analyze the status of a git branch.

    Args:
        branch_name: Name of branch to analyze (defaults to current branch)
        repo_path: Path to repository

    Returns:
        Dictionary containing branch status information

    Example:
        >>> status = analyze_branch_status('feature/new-feature')
        >>> print(f"Commits ahead: {status['ahead']}")
    """
    try:
        if repo_path is None:
            repo_path = get_git_root()

        if repo_path is None:
            return {}

        # Get current branch if not specified
        if branch_name is None:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            branch_name = result.stdout.strip()

        status = {
            'branch_name': branch_name,
            'exists': False,
            'current': False,
            'ahead': 0,
            'behind': 0,
            'uncommitted_changes': False,
            'last_commit': None,
            'author': None,
            'commit_message': None
        }

        # Check if branch exists
        result = subprocess.run(
            ['git', 'show-ref', '--verify', f'refs/heads/{branch_name}'],
            cwd=repo_path,
            capture_output=True
        )
        status['exists'] = (result.returncode == 0)

        if not status['exists']:
            return status

        # Check if this is the current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        current_branch = result.stdout.strip()
        status['current'] = (current_branch == branch_name)

        # Get ahead/behind counts
        try:
            result = subprocess.run(
                ['git', 'rev-list', '--left-right', '--count', f'origin/{branch_name}...{branch_name}'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                behind, ahead = result.stdout.strip().split()
                status['ahead'] = int(ahead)
                status['behind'] = int(behind)
        except Exception:
            pass

        # Check for uncommitted changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        status['uncommitted_changes'] = bool(result.stdout.strip())

        # Get last commit info
        result = subprocess.run(
            ['git', 'log', branch_name, '-1', '--format=%H|%an|%s'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            commit_hash, author, message = result.stdout.strip().split('|', 2)
            status['last_commit'] = commit_hash
            status['author'] = author
            status['commit_message'] = message

        return status

    except Exception as e:
        logger.error(f"Failed to analyze branch status: {e}")
        return {}


def generate_branch_report(repo_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Generate a comprehensive report of all branches in repository.

    Args:
        repo_path: Path to repository

    Returns:
        Dictionary containing branch report

    Example:
        >>> report = generate_branch_report()
        >>> print(f"Total branches: {report['total_branches']}")
    """
    try:
        if repo_path is None:
            repo_path = get_git_root()

        if repo_path is None:
            return {}

        # Get list of all branches
        result = subprocess.run(
            ['git', 'branch', '-a'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        branches = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if not line:
                continue
            # Remove * indicator for current branch
            if line.startswith('*'):
                line = line[1:].strip()
            # Skip remote references for now
            if 'remotes/' in line:
                continue
            branches.append(line)

        report = {
            'total_branches': len(branches),
            'branches': [],
            'current_branch': None
        }

        # Get current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        report['current_branch'] = result.stdout.strip()

        # Analyze each branch
        for branch in branches:
            branch_info = analyze_branch_status(branch, repo_path)
            report['branches'].append(branch_info)

        return report

    except Exception as e:
        logger.error(f"Failed to generate branch report: {e}")
        return {}


def get_branch_commits(branch_name: str,
                      limit: int = 10,
                      repo_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Get commit history for a branch.

    Args:
        branch_name: Name of branch
        limit: Maximum number of commits to return
        repo_path: Path to repository

    Returns:
        List of commit dictionaries
    """
    try:
        if repo_path is None:
            repo_path = get_git_root()

        if repo_path is None:
            return []

        result = subprocess.run(
            ['git', 'log', branch_name, f'-{limit}', '--format=%H|%an|%ae|%s|%ai'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|', 4)
            if len(parts) == 5:
                commit = {
                    'hash': parts[0],
                    'author_name': parts[1],
                    'author_email': parts[2],
                    'message': parts[3],
                    'date': parts[4]
                }
                commits.append(commit)

        return commits

    except Exception as e:
        logger.error(f"Failed to get branch commits: {e}")
        return []


def get_commit_history(branch_name: str,
                      limit: int = 10,
                      repo_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Alias for get_branch_commits for backward compatibility.

    Args:
        branch_name: Name of branch
        limit: Maximum number of commits
        repo_path: Path to repository

    Returns:
        List of commit dictionaries
    """
    return get_branch_commits(branch_name, limit, repo_path)


def categorize_commits(commits: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize commits by type (feat, fix, docs, etc.).

    Args:
        commits: List of commit dictionaries

    Returns:
        Dictionary mapping commit types to lists of commits
    """
    categories = {
        'features': [],
        'fixes': [],
        'docs': [],
        'refactor': [],
        'test': [],
        'chore': [],
        'other': []
    }

    for commit in commits:
        message = commit.get('message', '').lower()

        if message.startswith(('feat:', 'feature:')):
            categories['features'].append(commit)
        elif message.startswith('fix:'):
            categories['fixes'].append(commit)
        elif message.startswith('docs:'):
            categories['docs'].append(commit)
        elif message.startswith('refactor:'):
            categories['refactor'].append(commit)
        elif message.startswith('test:'):
            categories['test'].append(commit)
        elif message.startswith('chore:'):
            categories['chore'].append(commit)
        else:
            categories['other'].append(commit)

    return categories


def get_file_changes(commit_hash: str,
                    repo_path: Optional[Path] = None) -> List[str]:
    """
    Get list of files changed in a commit.

    Args:
        commit_hash: Commit hash
        repo_path: Path to repository

    Returns:
        List of changed file paths
    """
    try:
        if repo_path is None:
            repo_path = get_git_root()

        if repo_path is None:
            return []

        result = subprocess.run(
            ['git', 'show', '--name-only', '--format=', commit_hash],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
        return files

    except Exception as e:
        logger.error(f"Failed to get file changes for {commit_hash}: {e}")
        return []


__all__ = [
    'get_git_root',
    'analyze_branch_status',
    'generate_branch_report',
    'get_branch_commits',
    'get_commit_history',
    'categorize_commits',
    'get_file_changes'
]
