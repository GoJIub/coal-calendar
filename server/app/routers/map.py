from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import random

from ..database import get_db
from ..models import FireHistory, FirePrediction, Weather

# Создаем роутер
router = APIRouter()

@router.get("/map", status_code=status.HTTP_200_OK)
async def get_map_data(db: Session = Depends(get_db)):
    """
    Получение данных для карты с информацией о локациях, пожарах и прогнозах
    """
    try:
        # Получаем уникальные локации
        locations_query = """
            SELECT DISTINCT location FROM (
                SELECT location FROM fire_history
                UNION
                SELECT location FROM fire_predictions
            ) AS locations
        """
        locations_result = db.execute(locations_query).fetchall()
        
        location_data = []
        
        for loc in locations_result:
            location = loc[0]
            
            # Получаем последние данные о пожарах для этой локации
            fire_data = db.query(FireHistory).filter(
                FireHistory.location == location
            ).order_by(FireHistory.date.desc()).first()
            
            # Получаем последние прогнозы для этой локации
            prediction_data = db.query(FirePrediction).filter(
                FirePrediction.location == location
            ).order_by(FirePrediction.date.desc()).first()
            
            # Получаем последние погодные данные для этой локации
            weather_data = db.query(Weather).filter(
                Weather.location == location
            ).order_by(Weather.date.desc()).first()
            
            # Генерируем координаты для точки (в реальной системе будут геокоординаты)
            x = int(10 + random.random() * 80)
            y = int(10 + random.random() * 80)
            
            location_data.append({
                "location": location,
                "coordinates": {"x": x, "y": y},
                "fire": {
                    "date": fire_data.date.isoformat() if fire_data else None,
                    "has_fire": fire_data.has_fire if fire_data else False,
                    "severity": fire_data.severity if fire_data else 0
                } if fire_data else None,
                "prediction": {
                    "date": prediction_data.date.isoformat() if prediction_data else None,
                    "fire_probability": prediction_data.fire_probability if prediction_data else 0,
                    "risk_level": prediction_data.risk_level if prediction_data else "low"
                } if prediction_data else None,
                "weather": {
                    "date": weather_data.date.isoformat() if weather_data else None,
                    "temperature": weather_data.temperature if weather_data else 0,
                    "humidity": weather_data.humidity if weather_data else 0,
                    "wind_speed": weather_data.wind_speed if weather_data else 0,
                    "wind_direction": weather_data.wind_direction if weather_data else None
                } if weather_data else None
            })
        
        return {"success": True, "data": location_data}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении данных карты: {str(e)}"
        )