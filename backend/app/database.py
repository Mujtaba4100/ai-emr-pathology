from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.database_models import Base

# Create database URL
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False, connect_args={"connect_timeout": 5})

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

# Try to create tables on startup, but don't fail if PostgreSQL is unavailable
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"⚠️  Database tables could not be created (PostgreSQL may not be running): {str(e)[:100]}")

