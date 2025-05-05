from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, date

from ..database import get_db
from ..models import FireHistory, FirePrediction, Weather

# Создаем роутер
router = APIRouter()

@router.get("/statistics", status_code=status.HTTP_200_OK)
async def get_statistics(db: Session = Depends(get_db)):
    """
    Получение общей статистики о возгораниях, погоде и рисках
    """
    try:
        # Общее количество пожаров
        total_fires = db.query(func.count(FireHistory.id)).filter(
            FireHistory.has_fire == True
        ).scalar()
        
        # Последний пожар
        last_fire = db.query(FireHistory).filter(
            FireHistory.has_fire == True
        ).order_by(FireHistory.date.desc()).first()
        
        # Дни без пожаров (с последнего пожара)
        days_since_last_fire = 0
        if last_fire:
            days_since_last_fire = (datetime.now().date() - last_fire.date).days
        
        # Средняя температура
        avg_temp = db.query(func.avg(Weather.temperature)).scalar()
        
        # Текущий уровень риска (на основе последних прогнозов)
        current_risk_subquery = db.query(
            FirePrediction.risk_level, 
            func.count(FirePrediction.id).label('count')
        ).filter(
            FirePrediction.date >= datetime.now().date()
        ).group_by(
            FirePrediction.risk_level
        ).order_by(
            desc('count')
        ).first()
        
        current_risk_level = "Неизвестно"
        if current_risk_subquery:
            current_risk_level = current_risk_subquery[0]
        
        return {
            "success": True,
            "data": {
                "totalFires": total_fires or 0,
                "daysSinceLastFire": days_since_last_fire,
                "averageTemperature": round(avg_temp, 1) if avg_temp else 0,
                "currentRiskLevel": current_risk_level
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении статистики: {str(e)}"
        )