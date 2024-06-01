from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import Settings


settings = Settings()

engine = create_engine(
    url=settings.DATABASE_URL
)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db() -> Session:
    """
    initialize a db session instance and close it at the end
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()
