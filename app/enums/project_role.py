from enum import Enum


class ProjectRole(str, Enum):
    OWNER = "OWNER"
    PARTICIPANT = "PARTICIPANT"