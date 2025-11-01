import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

FLASK_ENV = os.getenv("FLASK_ENV", "tests")

DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "tu_password_aqui")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "blacklist_db")

if FLASK_ENV in ["local", "tests"]:
    DATABASE_URL = "sqlite:///emails.db"
    logger.info(f"Using SQLite database (FLASK_ENV={FLASK_ENV})")
else:
    DATABASE_URL = (
        f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@"
        f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    logger.info(f"Using PostgreSQL database (FLASK_ENV={FLASK_ENV}): {DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")

BEARER_TOKEN = os.getenv("BEARER_TOKEN", "my_static_token_123")
