"""Roles assigned to members of a project."""

from enum import Enum


class ProjectRole(str, Enum):
    """Supported project membership roles."""

    OWNER = "OWNER"
    PARTICIPANT = "PARTICIPANT"
