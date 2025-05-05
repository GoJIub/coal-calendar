from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

from ..database import Base

# SQLAlchemy модель
class CoalTemperature(Base):
    __tablename__ = "coal_temperature"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())

# Pydantic модели для API
class CoalTemperatureBase(BaseModel):
    date: date
    location: str
    temperature: float

class CoalTemperatureCreate(CoalTemperatureBase):
    pass

class CoalTemperatureResponse(CoalTemperatureBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True