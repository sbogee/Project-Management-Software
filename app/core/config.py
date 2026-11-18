"""Application configuration loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set in the environment or .env file")
    return value


DATABASE_URL = _required_env("DATABASE_URL")
SECRET_KEY = _required_env("SECRET_KEY")
