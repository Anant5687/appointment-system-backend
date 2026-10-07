from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.settings import settings

DATABASE_URL = settings.DATABASE_URL

ENGINE = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=ENGINE)

BASE = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    # BASE.metadata.drop_all(bind=ENGINE)
    BASE.metadata.create_all(bind=ENGINE)
