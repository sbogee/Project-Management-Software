"""Application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    "postgresql+psycopg2://admin:admin@localhost:5434/project_management"
)
SECRET_KEY = os.getenv("SECRET_KEY")
