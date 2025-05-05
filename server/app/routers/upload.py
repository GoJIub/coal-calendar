from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
import csv
from io import StringIO
from datetime import datetime
import os
import logging

from ..database import get_db
from ..models import (
    CoalTemperature, CoalTemperatureCreate,
    Weather, WeatherCreate,
    FireHistory, FireHistoryCreate
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем роутер
router = APIRouter()

@router.post("/upload/{type}", status_code=status.HTTP_200_OK)
async def upload_file(
    type: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    Загрузка CSV-файла с данными в базу данных.
    
    - **type**: Тип данных (coal, weather, fire_history)
    - **file**: CSV-файл с данными
    """
    logger.info(f"Начало загрузки файла: {file.filename}, тип: {type}")
    
    # Проверяем тип файла
    if not file.filename.endswith('.csv'):
        logger.error(f"Неправильный формат файла: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Разрешены только CSV-файлы"
        )
    
    try:
        # Создаем директорию для загрузки файлов, если она не существует
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        logger.info(f"Директория для загрузок: {upload_dir}")
        
        # Путь для сохранения файла
        file_path = os.path.join(upload_dir, f"{type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        # Читаем содержимое файла
        contents = await file.read()
        logger.info(f"Файл прочитан, размер: {len(contents)} байт")
        
        # Сохраняем файл локально для отладки
        with open(file_path, "wb") as f:
            f.write(contents)
        logger.info(f"Файл сохранен в: {file_path}")
        
        # Преобразуем байты в строку
        try:
            s = contents.decode('utf-8')
        except UnicodeDecodeError:
            # Пробуем другие кодировки, если utf-8 не работает
            try:
                s = contents.decode('cp1251')  # Кириллица Windows
            except UnicodeDecodeError:
                s = contents.decode('latin-1')  # Универсальная кодировка
        
        logger.info("Содержимое файла декодировано")
        
        # Используем pandas для чтения CSV
        try:
            df = pd.read_csv(StringIO(s), na_values=['NA', 'N/A', ''], keep_default_na=False)
            logger.info(f"Данные CSV загружены, строк: {len(df)}")
            
            # Выводим первые несколько строк для отладки
            logger.info(f"Первые строки данных: {df.head(2).to_dict()}")
        except Exception as e:
            logger.error(f"Ошибка при чтении CSV: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при чтении CSV-файла: {str(e)}"
            )
        
        # Обрабатываем данные в зависимости от типа файла
        if type == "coal":
            await process_coal_data(df, db)
        elif type == "weather":
            await process_weather_data(df, db)
        elif type == "fire_history":
            await process_fire_history_data(df, db)
        else:
            logger.error(f"Неизвестный тип файла: {type}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неизвестный тип файла. Поддерживаемые типы: coal, weather, fire_history"
            )
        
        logger.info("Данные успешно загружены в базу данных")
        return {"success": True, "message": "Файл успешно загружен и данные сохранены"}
    
    except Exception as e:
        logger.exception(f"Произошла ошибка при обработке файла: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обработке файла: {str(e)}"
        )

async def process_coal_data(df: pd.DataFrame, db: Session):
    """Обработка данных о температуре угля"""
    logger.info("Обработка данных о температуре угля")
    try:
        for _, row in df.iterrows():
            try:
                if isinstance(row['date'], str):
                    date_obj = datetime.strptime(row['date'], "%Y-%m-%d").date()
                else:
                    date_obj = row['date']
                
                coal_data = CoalTemperature(
                    date=date_obj,
                    location=str(row['location']),
                    temperature=float(row['temperature'])
                )
                db.add(coal_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке строки данных угля: {row}, ошибка: {str(e)}")
        
        db.commit()
        logger.info("Данные о температуре угля сохранены в базе")
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении данных о температуре угля: {str(e)}")
        raise

async def process_weather_data(df: pd.DataFrame, db: Session):
    """Обработка погодных данных"""
    logger.info("Обработка погодных данных")
    try:
        for _, row in df.iterrows():
            try:
                if isinstance(row['date'], str):
                    date_obj = datetime.strptime(row['date'], "%Y-%m-%d").date()
                else:
                    date_obj = row['date']
                
                weather_data = Weather(
                    date=date_obj,
                    location=str(row['location']),
                    temperature=float(row['temperature']),
                    humidity=float(row['humidity']),
                    wind_speed=float(row['wind_speed']),
                    wind_direction=str(row['wind_direction'])
                )
                db.add(weather_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке строки погодных данных: {row}, ошибка: {str(e)}")
        
        db.commit()
        logger.info("Погодные данные сохранены в базе")
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении погодных данных: {str(e)}")
        raise

async def process_fire_history_data(df: pd.DataFrame, db: Session):
    """Обработка данных об истории возгораний"""
    logger.info("Обработка данных об истории возгораний")
    try:
        for _, row in df.iterrows():
            try:
                if isinstance(row['date'], str):
                    date_obj = datetime.strptime(row['date'], "%Y-%m-%d").date()
                else:
                    date_obj = row['date']
                
                # Корректное преобразование has_fire в булево значение
                has_fire_value = row['has_fire']
                if isinstance(has_fire_value, str):
                    has_fire = has_fire_value.lower() in ['true', '1', 't', 'yes']
                else:
                    has_fire = bool(has_fire_value)
                
                fire_data = FireHistory(
                    date=date_obj,
                    location=str(row['location']),
                    has_fire=has_fire,
                    severity=int(row['severity'])
                )
                db.add(fire_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке строки данных о возгораниях: {row}, ошибка: {str(e)}")
        
        db.commit()
        logger.info("Данные об истории возгораний сохранены в базе")
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении данных об истории возгораний: {str(e)}")
        raise