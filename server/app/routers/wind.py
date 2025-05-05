from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from ..database import get_db
from ..models import Weather

# Создаем роутер
router = APIRouter()

@router.get("/wind", status_code=status.HTTP_200_OK)
async def get_wind_data(db: Session = Depends(get_db)):
    """
    Получение данных о розе ветров и статистике по ветру
    """
    try:
        # Получаем данные о направлении ветра и их количестве
        wind_directions = db.query(
            Weather.wind_direction,
            func.count(Weather.id).label('count')
        ).group_by(
            Weather.wind_direction
        ).all()
        
        # Конвертируем результаты sqlalchemy в словари
        directions_data = [
            {"wind_direction": direction, "count": count}
            for direction, count in wind_directions if direction
        ]
        
        # Средняя скорость ветра
        avg_wind_speed = db.query(func.avg(Weather.wind_speed)).scalar()
        
        # Максимальная скорость ветра
        max_wind_speed = db.query(func.max(Weather.wind_speed)).scalar()
        
        # Преобладающее направление ветра
        dominant_direction = db.query(
            Weather.wind_direction,
            func.count(Weather.id).label('count')
        ).group_by(
            Weather.wind_direction
        ).order_by(
            desc('count')
        ).first()
        
        return {
            "success": True,
            "data": {
                "directions": directions_data,
                "averageSpeed": round(avg_wind_speed, 1) if avg_wind_speed else 0,
                "maxSpeed": round(max_wind_speed, 1) if max_wind_speed else 0,
                "dominantDirection": dominant_direction[0] if dominant_direction else "Неизвестно"
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении данных о ветре: {str(e)}"
        )