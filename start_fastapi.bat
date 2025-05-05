 @echo off
echo Запуск приложения "Прогноз возгораний"...

REM Запускаем FastAPI бэкенд
start cmd /k "cd server && python -m uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload"

REM Даем бэкенду время на запуск
timeout /t 3

REM Запускаем фронтенд
start cmd /k "npm run dev"

echo Приложение запущено!
echo - Бэкенд: http://localhost:5000
echo - API документация: http://localhost:5000/docs
echo - Фронтенд: смотрите адрес в консоли Vite (обычно http://localhost:5173)
echo.
echo Для завершения работы закройте окна консоли
pause