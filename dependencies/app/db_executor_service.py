from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

# Инициализация базы данных и подключение к MariaDB
engine = create_engine("mariadb+mariadbconnector://root:root@db:3306/messenger_service")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Создадим генератор для сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
