import os
import subprocess
import time
import platform
import sys

def print_colored(text, color):
    """Выводит цветной текст в консоль."""
    colors = {
        'green': '\033[92m',
        'blue': '\033[94m',
        'yellow': '\033[93m',
        'end': '\033[0m'
    }
    if platform.system() == 'Windows':
        os.system('color')
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def main():
    """Запускает приложение 'Прогноз возгораний'."""
    print_colored("Запуск приложения 'Прогноз возгораний'...", 'blue')
    
    # Определение правильного расположения директорий
    server_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server')
    
    # Создаем команды для запуска процессов
    if platform.system() == 'Windows':
        backend_cmd = f'cd "{server_dir}" && python -m uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload'
        frontend_cmd = 'npm run dev'
    else:  # Linux/Mac
        backend_cmd = f'cd "{server_dir}" && python -m uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload'
        frontend_cmd = 'npm run dev'
    
    # Запускаем FastAPI бэкенд
    print_colored("Запуск FastAPI бэкенда...", 'green')
    backend_process = subprocess.Popen(
        backend_cmd, 
        shell=True,
        stdout=subprocess.PIPE if platform.system() != 'Windows' else None,
        stderr=subprocess.PIPE if platform.system() != 'Windows' else None,
        text=True
    )
    
    # Даем бэкенду время на запуск
    print_colored("Ожидание запуска бэкенда (3 секунды)...", 'yellow')
    time.sleep(3)
    
    # Запускаем фронтенд
    print_colored("Запуск фронтенда...", 'green')
    frontend_process = subprocess.Popen(
        frontend_cmd, 
        shell=True,
        stdout=subprocess.PIPE if platform.system() != 'Windows' else None,
        stderr=subprocess.PIPE if platform.system() != 'Windows' else None,
        text=True
    )
    
    print_colored("Приложение запущено!", 'blue')
    print_colored("- Бэкенд: http://localhost:5000", 'green')
    print_colored("- API документация: http://localhost:5000/docs", 'green')
    print_colored("- Фронтенд: смотрите адрес в консоли Vite (обычно http://localhost:5173)", 'green')
    print_colored("\nДля завершения работы нажмите Ctrl+C", 'yellow')
    
    try:
        # Ожидаем завершения обоих процессов (нажатие Ctrl+C приведет к исключению)
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print_colored("\nЗавершение работы приложения...", 'yellow')
        # Завершаем процессы
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main() 