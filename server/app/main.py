from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .database import engine, Base
from .routers import upload, calendar, map, statistics, wind, predict

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Прогноз возгораний на угольных складах",
    description="API для работы с данными о температуре угля, погоде и прогнозах возгораний",
    version="1.0.0"
)

# Настройка CORS для взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы со всех источников (для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(calendar.router, prefix="/api", tags=["Calendar"])
app.include_router(map.router, prefix="/api", tags=["Map"])
app.include_router(statistics.router, prefix="/api", tags=["Statistics"])
app.include_router(wind.router, prefix="/api", tags=["Wind"])
app.include_router(predict.router, prefix="/api", tags=["Predict"])

@app.get("/", tags=["Root"])
async def root():
    """
    Корневой эндпоинт, возвращает статус API
    """
    return {"status": "online", "message": "API прогноза возгораний готово к работе"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)