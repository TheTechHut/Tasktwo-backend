
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------
# DATABASE CONNECTION STRING
# ------------------------------
# For SQLite: local file database
SQLALCHEMY_DATABASE_URL = "sqlite:///./tickets.db"

# ------------------------------
# ENGINE SETUP
# ------------------------------
# The connect_args part is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ------------------------------
# SESSION LOCAL
# ------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------------------------------
# BASE CLASS
# ------------------------------
# This is used for model definitions
Base = declarative_base()

def get_db():
    """
    FastAPI dependency to get a database session.
    Closes the session after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()