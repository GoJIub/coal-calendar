from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
import calendar
import logging

from ..database import get_db
from ..models import CoalTemperature, Weather, FireHistory, FirePrediction

# Создаем роутер
router = APIRouter()

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@router.get("/calendar/{year}/{month}", status_code=status.HTTP_200_OK)
async def get_calendar_data(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """
    Получение данных для календаря за указанный месяц
    
    - **year**: Год (например, 2023)
    - **month**: Месяц (1-12)
    """
    try:
        # Проверяем корректность параметров
        if not (1 <= month <= 12):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Месяц должен быть от 1 до 12"
            )
        
        # Формируем даты начала и конца месяца
        start_date = date(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end_date = date(year, month, last_day)
        
        # Получаем данные из базы данных за указанный месяц
        fire_history = db.query(FireHistory).filter(
            FireHistory.date >= start_date,
            FireHistory.date <= end_date
        ).all()
        
        predictions = db.query(FirePrediction).filter(
            FirePrediction.date >= start_date,
            FirePrediction.date <= end_date
        ).all()
        
        weather = db.query(Weather).filter(
            Weather.date >= start_date,
            Weather.date <= end_date
        ).all()
        
        # Логирование результатов запросов
        logger.info(f"Fire history records: {len(fire_history)}")
        logger.info(f"Fire predictions records: {len(predictions)}")
        logger.info(f"Weather records: {len(weather)}")
        
        # Форматируем данные для календаря
        calendar_data = format_calendar_data(
            fire_history,
            predictions,
            weather,
            [],  # Пустой список для температуры угля
            year,
            month
        )
        
        return {"success": True, "data": calendar_data}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении данных календаря: {str(e)}"
        )

@router.get("/calendar/{year}/{month}/{day}", status_code=status.HTTP_200_OK)
async def get_calendar_data_with_day(
    year: int,
    month: int,
    day: int,
    db: Session = Depends(get_db)
):
    """
    Получение данных для календаря за указанный день

    - **year**: Год (например, 2023)
    - **month**: Месяц (1-12)
    - **day**: День (1-31)
    """
    try:
        # Проверяем корректность параметров
        if not (1 <= month <= 12):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Месяц должен быть от 1 до 12"
            )

        if not (1 <= day <= 31):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="День должен быть от 1 до 31"
            )

        # Формируем дату
        target_date = date(year, month, day)

        # Получаем данные из базы данных за указанный день
        fire_history = db.query(FireHistory).filter(FireHistory.date == target_date).all()
        predictions = db.query(FirePrediction).filter(FirePrediction.date == target_date).all()
        weather = db.query(Weather).filter(Weather.date == target_date).all()

        # Форматируем данные для календаря
        calendar_data = format_calendar_data(
            fire_history,
            predictions,
            weather,
            [],  # Пустой список для температуры угля
            year,
            month
        )

        return {"success": True, "data": calendar_data}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении данных календаря: {str(e)}"
        )

def format_calendar_data(fire_history, predictions, weather, coal_temp, year, month):
    """
    Форматирование данных для календаря
    """
    # Создаем словарь с данными для каждого дня месяца
    calendar_data = {}
    days_in_month = calendar.monthrange(year, month)[1]
    
    # Инициализируем структуру данных для каждого дня
    for day in range(1, days_in_month + 1):
        date_obj = date(year, month, day)
        date_str = date_obj.isoformat()
        
        calendar_data[date_str] = {
            "date": date_str,
            "fire": None,
            "prediction": None,
            "weather": None,
            "status": "unknown"
        }
    
    # Заполняем данные о пожарах
    for fire in fire_history:
        date_str = fire.date.isoformat()
        if date_str in calendar_data:
            calendar_data[date_str]["fire"] = {
                "hasFire": fire.has_fire,
                "severity": fire.severity
            }
    
    # Заполняем данные о прогнозах
    for prediction in predictions:
        date_str = prediction.date.isoformat()
        if date_str in calendar_data:
            calendar_data[date_str]["prediction"] = {
                "probability": prediction.fire_probability,
                "riskLevel": prediction.risk_level
            }
    
    # Заполняем данные о погоде
    for w in weather:
        date_str = w.date.isoformat()
        if date_str in calendar_data:
            calendar_data[date_str]["weather"] = {
                "temperature": w.temperature,
                "humidity": w.humidity,
                "windSpeed": w.wind_speed,
                "windDirection": w.wind_direction
            }
    
    # Определяем статус дня для календаря
    for date_str, day_data in calendar_data.items():
        status = "unknown"
        
        # Если есть данные о пожаре
        if day_data["fire"]:
            status = "fire" if day_data["fire"]["hasFire"] else "safe"
        # Если нет данных о пожаре, но есть прогноз
        elif day_data["prediction"]:
            if day_data["prediction"]["riskLevel"] == "high":
                status = "risk"
            elif day_data["prediction"]["riskLevel"] == "low":
                status = "safe"
            elif day_data["prediction"]["riskLevel"] == "medium":
                status = "risk"
        
        day_data["status"] = status
    
    return calendar_data