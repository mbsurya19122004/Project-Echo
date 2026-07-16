from __future__ import annotations

from typing import Any
import subprocess

from config import DEFAULT_TIMEOUT

from .safety import is_dangerous

import shlex
import time

def execute_bash(command: str,timeout: int = DEFAULT_TIMEOUT,confirm_dangerous: bool = False,) -> dict[str, Any]:
    """
    Execute an arbitrary Bash command on the local machine.

    Use this tool only as a fallback when the requested task cannot be completed
    using a more specific tool. Prefer dedicated tools for actions such as window
    management, process management, file operations, or other supported system
    functions, as they are safer and provide more reliable results.

    This tool is intended for general shell operations that have no dedicated tool
    available.

    Args:
        command: The Bash command to execute.
        timeout: Maximum execution time in seconds.
        confirm_dangerous: Must be True to allow execution of commands identified
            as potentially destructive. If False, dangerous commands are blocked.

    Returns:
        A dictionary containing the execution result:

        {
            "success": bool,      # True if the command exited with return code 0
            "stdout": str,        # Standard output from the command
            "stderr": str,        # Standard error from the command
            "returncode": int     # Process exit code (-1 on internal failure)
        }

    Notes:
        - Do not use this tool if another available tool can accomplish the task.
        - Do not assume the command succeeded; always inspect the returned values.
        - Treat success as `success == True`, not merely the absence of stderr.
    """
    print(f"execute_bash : {command}")
    if is_dangerous(command) and not confirm_dangerous:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Dangerous command blocked. Ask for confirmation first.",
            "returncode": -1,
        }

    try:
        result = subprocess.run(
            "cd ~ && "+command,
            shell=True,
            executable="/bin/bash",
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out.",
            "returncode": -1,
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
        }

def start_process(command: str) -> dict:
    """
    Launch a process and verify that it successfully started.

    The command is executed in a shell using ``subprocess.Popen``. After a
    short delay, the function checks the system process list with ``pgrep -f``
    to determine whether the executable is running.

    This function is intended primarily for launching long-running processes
    such as GUI applications (e.g. Firefox, VS Code, Kitty) or background
    services. It is not suitable for short-lived commands that are expected to
    exit immediately.

    Args:
        command: The shell command used to start the process.

    Returns:
        A dictionary containing the execution result.

        On success:
            {
                "status": "success",
                "running": True,
                "pids": list[int],
                "message": "<executable> is running."
            }

        On failure:
            {
                "status": "error",
                "running": False,
                "message": "<executable> failed to start."
            }

    Notes:
        - Verification is performed using ``pgrep -f <executable>``.
        - The command's stdout and stderr are discarded.
        - The function waits approximately two seconds before checking whether
          the process is running.
        - A successful return indicates that at least one matching process was
          found, not necessarily that the application is fully initialized.
    """
    print(f"start_process : {command}")
    executable = shlex.split(command)[0]

    subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    time.sleep(2)

    check = subprocess.run(
        ["pgrep", "-f", executable],
        capture_output=True,
        text=True,
    )

    if check.returncode == 0:
        pids = [int(pid) for pid in check.stdout.split()]
        return {
            "status": "success",
            "running": True,
            "pids": pids,
            "message": f"{executable} is running.",
        }

    return {
        "status": "error",
        "running": False,
        "message": f"{executable} failed to start.",
    }