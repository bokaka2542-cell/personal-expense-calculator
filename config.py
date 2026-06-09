import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    raw_db_url = os.environ.get("DATABASE_URL", "")
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql+pg8000://", 1)
    elif raw_db_url.startswith("postgresql://"):
        raw_db_url = raw_db_url.replace("postgresql://", "postgresql+pg8000://", 1)

    SQLALCHEMY_DATABASE_URI = raw_db_url or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'expenses.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
