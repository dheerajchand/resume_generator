"""
Shell command execution utilities for siege_utilities.
Provides safe subprocess execution with proper error handling.
"""

import subprocess
import logging
from typing import Union, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

CommandType = Union[str, List[str]]


def run_subprocess(command: CommandType,
                   shell: bool = True,
                   cwd: Optional[Union[str, Path]] = None,
                   timeout: Optional[int] = None,
                   capture_output: bool = True,
                   check: bool = False,
                   encoding: str = 'utf-8') -> str:
    """
    Run a subprocess command and return output.

    Args:
        command: Command to execute (string or list)
        shell: Whether to use shell execution
        cwd: Working directory
        timeout: Timeout in seconds
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero return code
        encoding: Output encoding

    Returns:
        Command output as string (stdout if success, stderr if failure)

    Example:
        >>> output = run_subprocess(['ls', '-la'])
        >>> output = run_subprocess('echo "hello"', shell=True)
    """
    try:
        logger.debug(f"Executing command: {command}")

        # Execute subprocess
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            shell=shell,
            cwd=cwd
        )

        # Wait for completion with timeout
        stdout_data, stderr_data = process.communicate(timeout=timeout)

        # Decode output
        if stdout_data:
            stdout_str = stdout_data.decode(encoding) if isinstance(stdout_data, bytes) else stdout_data
        else:
            stdout_str = ''

        if stderr_data:
            stderr_str = stderr_data.decode(encoding) if isinstance(stderr_data, bytes) else stderr_data
        else:
            stderr_str = ''

        # Check return code
        if process.returncode == 0:
            logger.debug(f"Command succeeded: {command}")
            return stdout_str
        else:
            logger.warning(f"Command failed with code {process.returncode}: {command}")
            if check:
                raise subprocess.CalledProcessError(
                    process.returncode, command, stdout_str, stderr_str
                )
            return stderr_str

    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {command}")
        process.kill()
        raise
    except Exception as e:
        logger.error(f"Failed to execute command {command}: {e}")
        raise


def run_shell_command(command: str,
                      cwd: Optional[Union[str, Path]] = None,
                      timeout: Optional[int] = None) -> Tuple[int, str, str]:
    """
    Run a shell command and return exit code, stdout, and stderr.

    Args:
        command: Shell command to execute
        cwd: Working directory
        timeout: Timeout in seconds

    Returns:
        Tuple of (exit_code, stdout, stderr)

    Example:
        >>> code, out, err = run_shell_command('ls -la')
        >>> if code == 0:
        ...     print(f"Success: {out}")
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            timeout=timeout,
            capture_output=True,
            text=True
        )

        return result.returncode, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {command}")
        return -1, '', 'Command timed out'
    except Exception as e:
        logger.error(f"Failed to execute command {command}: {e}")
        return -1, '', str(e)


def execute_command_list(commands: List[str],
                        stop_on_error: bool = True,
                        cwd: Optional[Union[str, Path]] = None) -> List[Tuple[str, int, str]]:
    """
    Execute a list of commands sequentially.

    Args:
        commands: List of commands to execute
        stop_on_error: Whether to stop on first error
        cwd: Working directory

    Returns:
        List of tuples (command, exit_code, output)

    Example:
        >>> commands = ['mkdir -p test', 'cd test', 'touch file.txt']
        >>> results = execute_command_list(commands)
    """
    results = []

    for command in commands:
        try:
            code, stdout, stderr = run_shell_command(command, cwd=cwd)
            output = stdout if code == 0 else stderr
            results.append((command, code, output))

            if code != 0 and stop_on_error:
                logger.warning(f"Stopping execution due to error in: {command}")
                break

        except Exception as e:
            logger.error(f"Failed to execute command {command}: {e}")
            results.append((command, -1, str(e)))
            if stop_on_error:
                break

    return results


def check_command_exists(command: str) -> bool:
    """
    Check if a command exists in the system PATH.

    Args:
        command: Command name to check

    Returns:
        True if command exists, False otherwise

    Example:
        >>> if check_command_exists('git'):
        ...     print("Git is installed")
    """
    try:
        result = subprocess.run(
            ['which', command],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def get_command_output(command: CommandType,
                       shell: bool = True,
                       cwd: Optional[Union[str, Path]] = None) -> Optional[str]:
    """
    Get command output, return None on error.

    Args:
        command: Command to execute
        shell: Whether to use shell
        cwd: Working directory

    Returns:
        Command output or None if failed
    """
    try:
        return run_subprocess(command, shell=shell, cwd=cwd, check=False)
    except Exception as e:
        logger.error(f"Failed to get command output: {e}")
        return None


__all__ = [
    'run_subprocess',
    'run_shell_command',
    'execute_command_list',
    'check_command_exists',
    'get_command_output'
]
