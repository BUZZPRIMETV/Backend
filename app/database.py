from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine - manages connections to PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,  # Connection pool for scalability
    max_overflow=20  # Extra connections when pool is full
)

# Session factory - creates database sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our database models
Base = declarative_base()

# Dependency to get database session in routes
def get_db():
    """
    Creates a database session for each request and closes it after.
    This is used with FastAPI's dependency injection.
    """
    db = SessionLocal()
    try:
        yield db  # Provide session to route
    finally:
        db.close()  # Always close after request