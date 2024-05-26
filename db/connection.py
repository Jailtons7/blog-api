from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import Settings


settings = Settings()

engine = create_engine(
    url=settings.DATABASE_URL,
    connect_args={'check_same_thread': False}
)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
