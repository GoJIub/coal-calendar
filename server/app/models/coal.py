from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

from ..database import Base

# SQLAlchemy модель
class CoalTemperature(Base):
    __tablename__ = f"coal_temperature_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    id = Column(Integer, primary_key=True, index=True)
    warehouse = Column(Integer, nullable=False)
    stack = Column(Integer, nullable=False)
    grade = Column(String, nullable=False)
    max_temp = Column(Float, nullable=False)
    picket = Column(String, nullable=False)
    act_date = Column(Date, nullable=False)

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