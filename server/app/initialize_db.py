from .database import engine, Base

def initialize_database():
    """Создание всех таблиц в базе данных"""
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы.")

if __name__ == "__main__":
    initialize_database()