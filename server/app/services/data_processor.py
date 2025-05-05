import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO

def process_csv_data(content, file_type):
    """
    Обработка CSV данных и преобразование в pandas DataFrame
    
    Параметры:
    - content: строковое содержимое CSV файла
    - file_type: тип данных ('coal', 'weather', 'fire_history')
    
    Возвращает:
    - pandas DataFrame с обработанными данными
    """
    try:
        df = pd.read_csv(StringIO(content))
        
        # Проверка наличия необходимых колонок
        if file_type == 'coal' and not all(col in df.columns for col in ['date', 'location', 'temperature']):
            raise ValueError("CSV-файл с данными о температуре угля должен содержать колонки: date, location, temperature")
        
        elif file_type == 'weather' and not all(col in df.columns for col in ['date', 'location', 'temperature', 'humidity', 'wind_speed', 'wind_direction']):
            raise ValueError("CSV-файл с погодными данными должен содержать колонки: date, location, temperature, humidity, wind_speed, wind_direction")
        
        elif file_type == 'fire_history' and not all(col in df.columns for col in ['date', 'location', 'has_fire', 'severity']):
            raise ValueError("CSV-файл с историей возгораний должен содержать колонки: date, location, has_fire, severity")
        
        # Преобразование даты
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Преобразование числовых данных
        if 'temperature' in df.columns:
            df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        
        if 'humidity' in df.columns:
            df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
        
        if 'wind_speed' in df.columns:
            df['wind_speed'] = pd.to_numeric(df['wind_speed'], errors='coerce')
        
        if 'severity' in df.columns:
            df['severity'] = pd.to_numeric(df['severity'], errors='coerce').astype(int)
        
        # Преобразование булевых данных
        if 'has_fire' in df.columns:
            df['has_fire'] = df['has_fire'].map(lambda x: True if str(x).lower() in ['true', '1', 't', 'yes'] else False)
        
        return df
    
    except Exception as e:
        raise ValueError(f"Ошибка при обработке CSV-файла: {str(e)}")

def validate_csv_data(df, file_type):
    """
    Проверка корректности данных в DataFrame
    
    Параметры:
    - df: pandas DataFrame с данными
    - file_type: тип данных ('coal', 'weather', 'fire_history')
    
    Возвращает:
    - булево значение (True если данные корректны)
    - сообщение об ошибке (пустая строка если данные корректны)
    """
    if df.empty:
        return False, "CSV-файл не содержит данных"
    
    # Проверка на наличие пропущенных значений
    missing_columns = []
    
    if file_type == 'coal':
        for col in ['date', 'location', 'temperature']:
            if df[col].isnull().any():
                missing_columns.append(col)
    
    elif file_type == 'weather':
        for col in ['date', 'location', 'temperature', 'humidity', 'wind_speed']:
            if df[col].isnull().any():
                missing_columns.append(col)
    
    elif file_type == 'fire_history':
        for col in ['date', 'location', 'has_fire', 'severity']:
            if df[col].isnull().any():
                missing_columns.append(col)
    
    if missing_columns:
        return False, f"В CSV-файле есть пропущенные значения в колонках: {', '.join(missing_columns)}"
    
    return True, ""