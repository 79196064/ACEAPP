from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL del database SQLite
DATABASE_URL = "sqlite:///./aceapp.db"

# Creazione del motore
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Sessione del database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base per i modelli SQLAlchemy
Base = declarative_base()


def get_db():
    """Fornisce una sessione SQLAlchemy e la chiude al termine della richiesta."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
