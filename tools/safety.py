import re

DANGEROUS_PATTERNS = [
    r"\brm\b",
    r"\bdd\b",
    r"\bmkfs",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bpoweroff\b",
    r"\bhalt\b",
    r"\bchmod\b",
    r"\bchown\b",
    r"\bmv\b",
    r"\bcp\b",
    r"\buserdel\b",
    r"\bgroupdel\b",
    r"\bpacman\s+-R",
    r"\bsudo\b",
]


def is_dangerous(command: str) -> bool:
    """
    Determine whether a shell command is potentially destructive.

    The command is checked against a predefined list of regular
    expression patterns representing operations that may modify,
    delete, or otherwise affect the system. This is used to require
    explicit user confirmation before executing such commands.

    Args:
        command: The shell command to inspect.

    Returns:
        True if the command matches any dangerous pattern, otherwise False.
    """
    return any(re.search(pattern, command) for pattern in DANGEROUS_PATTERNS)