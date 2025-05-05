from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

from ..database import Base

# SQLAlchemy модель
class Weather(Base):
    __tablename__ = f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}"  # Уникальное имя таблицы с номером

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date = Column(DateTime, nullable=False)
    t = Column(Float, nullable=False)
    p = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    precipitation = Column(Float, nullable=True)
    wind_dir = Column(Integer, nullable=True)
    v_avg = Column(Float, nullable=True)
    v_max = Column(Float, nullable=True)
    cloudcover = Column(Integer, nullable=True)
    weather_code = Column(Integer, nullable=True)

# Pydantic модели для API
class WeatherBase(BaseModel):
    date: date
    location: str
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: Optional[str] = None

class WeatherCreate(WeatherBase):
    pass

class WeatherResponse(WeatherBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True