from __future__ import annotations

import json
from typing import Any

from .bash import execute_bash


def getAllWindows() -> list[dict[str, Any]]:
    """
    Retrieve all currently mapped Hyprland windows.

    Returns:
        A list of dictionaries, one for each window, containing:
            - address (str): Unique Hyprland window address.
            - title (str): Window title.
            - class (str): Window class/application.
            - workspace (str): Workspace name.
            - workspace_id (int): Workspace ID.
            - pid (int): Process ID.
            - floating (bool): Whether the window is floating.
            - fullscreen (bool): Fullscreen state.
            - mapped (bool): Whether the window is mapped.
            - hidden (bool): Whether the window is hidden.
            - at (list[int]): Window position [x, y].
            - size (list[int]): Window size [width, height].

    Raises:
        RuntimeError: If Hyprland fails to return client information or
            the JSON output cannot be parsed.
    """
    result = execute_bash("hyprctl clients -j")

    if not result["success"]:
        raise RuntimeError(result["stderr"])

    clients = json.loads(result["stdout"])

    windows = []

    for client in clients:
        windows.append(
            {
                "address": client.get("address"),
                "title": client.get("title"),
                "class": client.get("class"),
                "workspace": client.get("workspace", {}).get("name"),
                "workspace_id": client.get("workspace", {}).get("id"),
                "pid": client.get("pid"),
                "floating": client.get("floating"),
                "fullscreen": client.get("fullscreen"),
                "mapped": client.get("mapped"),
                "hidden": client.get("hidden"),
                "at": client.get("at"),
                "size": client.get("size"),
            }
        )

    return windows


def fullscreen(address: str) -> None:
    """
    Set a Hyprland window to fullscreen.

    The window is first focused using its Hyprland address, then switched
    to fullscreen mode.

    Args:
        address: The Hyprland window address (e.g. "0x55a8c1b8d2f0").

    Returns:
        None
    """
    execute_bash(
        f'''hyprctl eval 'hl.dispatch(hl.dsp.focus({{ window = "address:{address}" }}))' && \
hyprctl eval 'hl.dispatch(hl.dsp.window.fullscreen({{ mode = "fullscreen", action = "set" }}))' '''
    )