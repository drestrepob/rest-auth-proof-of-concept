from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True, future=True)
base = declarative_base()
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
