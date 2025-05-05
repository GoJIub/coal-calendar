from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
from datetime import datetime, timedelta
import random

from ..database import get_db
from ..models import (
    CoalTemperature, Weather, FireHistory, 
    FirePrediction, FirePredictionCreate
)
from ..services.predict import predict_fires

# Создаем роутер
router = APIRouter()

@router.post("/predict", status_code=status.HTTP_200_OK)
async def generate_predictions(db: Session = Depends(get_db)):
    """
    Создание прогнозов возгораний на основе имеющихся данных
    """
    try:
        # Получаем данные для модели
        coal_temp_data = db.query(CoalTemperature).all()
        weather_data = db.query(Weather).all()
        fire_history_data = db.query(FireHistory).all()
        
        if not coal_temp_data or not weather_data or not fire_history_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недостаточно данных для создания прогнозов"
            )
        
        # Преобразуем данные в pandas DataFrames для модели ML
        coal_df = pd.DataFrame([{
            'date': data.date,
            'location': data.location,
            'temperature': data.temperature
        } for data in coal_temp_data])
        
        weather_df = pd.DataFrame([{
            'date': data.date,
            'location': data.location,
            'temperature': data.temperature,
            'humidity': data.humidity,
            'wind_speed': data.wind_speed,
            'wind_direction': data.wind_direction
        } for data in weather_data])
        
        fire_df = pd.DataFrame([{
            'date': data.date,
            'location': data.location,
            'has_fire': data.has_fire,
            'severity': data.severity
        } for data in fire_history_data])
        
        # Получаем прогнозы от модели
        # В будущем вызовем ML-модель
        predictions = generate_mock_predictions(coal_df, weather_df, fire_df)
        
        # Сохраняем прогнозы в базу данных
        saved_predictions = []
        for pred in predictions:
            # Проверяем, нет ли уже прогноза на эту дату и локацию
            existing = db.query(FirePrediction).filter(
                FirePrediction.date == pred['date'],
                FirePrediction.location == pred['location']
            ).first()
            
            if existing:
                existing.fire_probability = pred['probability']
                existing.risk_level = pred['risk_level']
                db.add(existing)
                saved_predictions.append(existing)
            else:
                new_prediction = FirePrediction(
                    date=pred['date'],
                    location=pred['location'],
                    fire_probability=pred['probability'],
                    risk_level=pred['risk_level']
                )
                db.add(new_prediction)
                saved_predictions.append(new_prediction)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Прогнозы успешно созданы и сохранены",
            "predictions": [
                {
                    "date": pred.date.isoformat(),
                    "location": pred.location,
                    "probability": pred.fire_probability,
                    "risk_level": pred.risk_level
                } for pred in saved_predictions
            ]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании прогнозов: {str(e)}"
        )

def generate_mock_predictions(coal_df, weather_df, fire_df):
    """
    Генерирует имитационные прогнозы (будет заменена на реальную модель)
    """
    predictions = []
    
    # Получаем уникальные локации
    locations = fire_df['location'].unique()
    
    # Получаем последнюю дату из истории
    latest_date = fire_df['date'].max()
    current_date = datetime.combine(latest_date, datetime.min.time())
    
    # Генерируем прогнозы на следующие 30 дней
    for i in range(1, 31):
        pred_date = current_date + timedelta(days=i)
        
        for location in locations:
            probability = random.random()  # Случайная вероятность для имитации
            
            # Определяем уровень риска на основе вероятности
            if probability > 0.7:
                risk_level = "high"
            elif probability > 0.4:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            predictions.append({
                "date": pred_date.date(),
                "location": location,
                "probability": probability,
                "risk_level": risk_level
            })
    
    return predictions