from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

from ..database import Base

# SQLAlchemy модель
class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_direction = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

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