from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings


settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
Sessionlocal = sessionmaker[Session](bind=engine)


# подключение к БД
def get_db():
    """Функция для инъекции сессии БД"""
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()