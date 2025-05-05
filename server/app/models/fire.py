from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

from ..database import Base

# SQLAlchemy модель истории возгораний
class FireHistory(Base):
    __tablename__ = "fire_history"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    creation_date = Column(DateTime, nullable=False)
    cargo = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    warehouse = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    initial_stack_date = Column(DateTime, nullable=True)
    stack = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

# SQLAlchemy модель прогнозов возгораний
class FirePrediction(Base):
    __tablename__ = "fire_predictions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    fire_probability = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

# Pydantic модели для API
class FireHistoryBase(BaseModel):
    date: date
    location: str
    has_fire: bool
    severity: int

class FireHistoryCreate(FireHistoryBase):
    pass

class FireHistoryResponse(FireHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FirePredictionBase(BaseModel):
    date: date
    location: str
    fire_probability: float
    risk_level: str

class FirePredictionCreate(FirePredictionBase):
    pass

class FirePredictionResponse(FirePredictionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True