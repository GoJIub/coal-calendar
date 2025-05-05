from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Строка подключения к базе данных
DATABASE_URL = "postgresql://postgres:ZEcOwNDTbOQDjLHchZKyhEOeEOfnEcFW@switchyard.proxy.rlwy.net:44380/railway"

# Создание движка SQLAlchemy для взаимодействия с базой данных
engine = create_engine(DATABASE_URL)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

# Функция-зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()