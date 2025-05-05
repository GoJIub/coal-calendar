from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
import csv
from io import StringIO
from datetime import datetime
import os
import logging

from ..database import get_db, Base
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

@router.post("/upload/{type}")
async def upload_file(type: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    logger.info(f"Начало загрузки файла: {file.filename}, тип: {type}")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        contents = await file.read()
        s = contents.decode('utf-8')
        df = pd.read_csv(StringIO(s))
        
        if type == "weather":
            await process_weather_data(df, db)
        elif type == "fire_history":
            await process_fire_history_data(df, db)
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")

        return {"message": "File uploaded successfully"}
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_coal_data(df: pd.DataFrame, db: Session):
    """Обработка данных о температуре угля"""
    logger.info("Обработка данных о температуре угля")
    try:
        # Удаляем лишние пробелы из названий столбцов
        df.columns = df.columns.str.strip()

        for index, row in df.iterrows():
            try:
                # Проверяем наличие всех необходимых столбцов
                required_columns = ['warehouse', 'stack', 'grade', 'max_temp', 'picket', 'act_date']
                for col in required_columns:
                    if col not in row or pd.isna(row[col]):
                        raise ValueError(f"Отсутствует значение в столбце '{col}' на строке {index}")

                # Преобразуем act_date в объект даты
                if isinstance(row['act_date'], str):
                    act_date_obj = datetime.strptime(row['act_date'].strip(), "%Y-%m-%d").date()
                else:
                    act_date_obj = row['act_date']

                # Создаем объект CoalTemperature
                coal_data = CoalTemperature(
                    warehouse=int(row['warehouse']),
                    stack=int(row['stack']),
                    grade=row['grade'].strip(),
                    max_temp=float(row['max_temp']),
                    picket=row['picket'].strip(),
                    act_date=act_date_obj
                )
                db.add(coal_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке строки {index}: {row.to_dict()}, ошибка: {str(e)}")

        db.commit()
        logger.info("Данные о температуре угля сохранены в базе")
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении данных о температуре угля: {str(e)}")
        raise

async def process_weather_data(df: pd.DataFrame, db: Session):
    """Обработка данных о погоде"""
    logger.info("Обработка данных о погоде")
    try:
        # Удаляем лишние пробелы из названий столбцов
        df.columns = df.columns.str.strip()

        for index, row in df.iterrows():
            try:
                # Проверяем наличие всех необходимых столбцов
                required_columns = ['date', 't', 'p', 'humidity', 'precipitation', 'wind_dir', 'v_avg', 'v_max', 'cloudcover', 'weather_code']
                for col in required_columns:
                    if col not in df.columns or pd.isna(row[col]):
                        raise ValueError(f"Отсутствует значение в столбце '{col}' на строке {index}")

                # Преобразуем date в объект даты и времени
                date_obj = datetime.strptime(row['date'].strip(), "%Y-%m-%d %H:%M:%S") if not pd.isna(row['date']) else None

                # Создаем объект Weather
                weather_data = Weather(
                    date=date_obj,
                    temperature=float(row['t']) if not pd.isna(row['t']) else None,
                    pressure=float(row['p']) if not pd.isna(row['p']) else None,
                    humidity=float(row['humidity']) if not pd.isna(row['humidity']) else None,
                    precipitation=float(row['precipitation']) if not pd.isna(row['precipitation']) else None,
                    wind_dir=int(row['wind_dir']) if not pd.isna(row['wind_dir']) else None,
                    wind_avg=float(row['v_avg']) if not pd.isna(row['v_avg']) else None,
                    wind_max=float(row['v_max']) if not pd.isna(row['v_max']) else None,
                    cloudcover=int(row['cloudcover']) if not pd.isna(row['cloudcover']) else None,
                    weather_code=int(row['weather_code']) if not pd.isna(row['weather_code']) else None
                )
                db.add(weather_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке строки {index}: {row.to_dict()}, ошибка: {str(e)}")

        db.commit()
        logger.info("Данные о погоде сохранены в базе")
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении данных о погоде: {str(e)}")
        raise

async def process_fire_history_data(df: pd.DataFrame, db: Session):
    """Обработка данных об истории возгораний"""
    logger.info("Обработка данных об истории возгораний")
    try:
        # Удаляем лишние пробелы из названий столбцов
        df.columns = df.columns.str.strip()

        for index, row in df.iterrows():
            try:
                # Проверяем наличие всех необходимых столбцов
                required_columns = ['creation_date', 'cargo', 'weight', 'warehouse', 'start_date', 'end_date', 'initial_stack_date', 'stack']
                for col in required_columns:
                    if col not in df.columns or pd.isna(row[col]):
                        raise ValueError(f"Отсутствует значение в столбце '{col}' на строке {index}")

                # Преобразуем даты в объекты даты и времени
                creation_date_obj = datetime.strptime(row['creation_date'].strip(), "%Y-%m-%d")
                start_date_obj = datetime.strptime(row['start_date'].strip(), "%Y-%m-%d %H:%M:%S") if not pd.isna(row['start_date']) else None
                end_date_obj = datetime.strptime(row['end_date'].strip(), "%Y-%m-%d %H:%M:%S") if not pd.isna(row['end_date']) else None
                initial_stack_date_obj = datetime.strptime(row['initial_stack_date'].strip(), "%Y-%m-%d %H:%M:%S") if not pd.isna(row['initial_stack_date']) else None

                # Создаем объект FireHistory
                fire_data = FireHistory(
                    creation_date=creation_date_obj,
                    cargo=row['cargo'].strip() if not pd.isna(row['cargo']) else None,
                    weight=float(row['weight']) if not pd.isna(row['weight']) else None,
                    warehouse=int(row['warehouse']) if not pd.isna(row['warehouse']) else None,
                    start_date=start_date_obj,
                    end_date=end_date_obj,
                    initial_stack_date=initial_stack_date_obj,
                    stack=int(row['stack']) if not pd.isna(row['stack']) else None
                )
                db.add(fire_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке строки {index}: {row.to_dict()}, ошибка: {str(e)}")

        db.commit()
        logger.info("Данные об истории возгораний сохранены в базе")
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении данных об истории возгораний: {str(e)}")
        raise

async def process_temperature_data(df: pd.DataFrame, db: Session):
    """Обработка данных о температуре"""
    logger.info("Обработка данных о температуре")
    try:
        for _, row in df.iterrows():
            try:
                logger.info(f"Обработка строки: {row.to_dict()}")  # Логируем каждую строку
                temperature_data = CoalTemperature(
                    warehouse=int(row["warehouse"]),
                    stack=int(row["stack"]),
                    grade=row["grade"],
                    max_temp=float(row["max_temp"]),
                    picket=row["picket"],
                    act_date=row["act_date"]
                )
                db.add(temperature_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке строки данных о температуре: {row.to_dict()}, ошибка: {str(e)}")
        
        db.commit()
        logger.info("Данные о температуре сохранены в базе")
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении данных о температуре: {str(e)}")
        raise