import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Environment
    FLASK_ENV = os.getenv("FLASK_ENV") or os.getenv("NODE_ENV") or "production"
    PORT = int(os.getenv("PORT", "5000"))

    # External API (kept for reference/use by other modules)
    EXTERNAL_DB_API_URL = os.getenv("EXTERNAL_DB_API_URL")
    EXTERNAL_DB_API_KEY = os.getenv("EXTERNAL_DB_API_KEY")

    # Backend
    DATABASE_URL = os.getenv("DATABASE_URL")
    # Allow using EXTERNAL_DB_API_KEY as API key if API_KEY is not set
    API_KEY = os.getenv("API_KEY") or os.getenv("EXTERNAL_DB_API_KEY")

    # Database connection pool settings
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    
    # Feature flags
    USE_DUMMY_DATA = os.getenv("USE_DUMMY_DATA", "false").strip().lower() in {"1", "true", "yes", "on"}
    
