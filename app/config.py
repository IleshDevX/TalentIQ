"""
TalentIQ — Application Configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Settings:
    APP_NAME: str = "TalentIQ"
    APP_VERSION: str = "2.0.0"

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent   # E:\08 TalentIQ
    DATASETS_DIR: Path = BASE_DIR / "datasets"

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:8501",   # Streamlit default
        "http://127.0.0.1:8501",
    ]

    # Model config
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    TOP_K_ROLES: int = 5

    # Upload limits
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set[str] = {".pdf", ".docx"}


settings = Settings()
