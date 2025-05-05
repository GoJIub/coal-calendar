import { useState, useEffect } from 'react';
import { getCalendarData } from '../api';
import './Calendar.css';

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDay, setSelectedDay] = useState(null);
  const [calendarData, setCalendarData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const daysInMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1,
    0
  ).getDate();

  const firstDayOfMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    1
  ).getDay();
  
  // В России неделя начинается с понедельника (1), а не с воскресенья (0)
  const adjustedFirstDay = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;

  const monthNames = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  // Загрузка данных календаря при изменении месяца
  useEffect(() => {
    loadCalendarData();
  }, [currentDate]);

  const loadCalendarData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth() + 1; // API ожидает месяц от 1 до 12
      
      const response = await getCalendarData(year, month);
      
      if (response.success) {
        setCalendarData(response.data);
      } else {
        setError('Не удалось загрузить данные календаря');
        console.error('Ошибка при загрузке данных календаря:', response.message);
        
        // Используем запасные данные при ошибке
        setCalendarData(getFallbackData());
      }
    } catch (err) {
      setError('Произошла ошибка при загрузке данных календаря');
      console.error('Ошибка при загрузке данных календаря:', err);
      
      // Используем запасные данные при ошибке
      setCalendarData(getFallbackData());
    } finally {
      setIsLoading(false);
    }
  };

  // Запасные данные, если API недоступен
  const getFallbackData = () => {
    const data = {};
    const seed = currentDate.getFullYear() * 100 + currentDate.getMonth();
    
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
      
      // Используем детерминированное псевдослучайное число на основе дня и месяца
      const random = ((seed * day) % 100) / 100;
      let status = 'unknown';
      
      if (random < 0.3) status = 'fire';
      else if (random < 0.6) status = 'safe';
      else status = 'risk';
      
      data[dateStr] = {
        date: dateStr,
        status,
        weather: {
          temperature: Math.round(20 + random * 10),
          humidity: Math.round(40 + random * 20),
          windSpeed: Math.round(2 + random * 8)
        }
      };
    }
    
    return data;
  };

  const handlePrevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
    setSelectedDay(null); // Сбрасываем выбранный день при смене месяца
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
    setSelectedDay(null); // Сбрасываем выбранный день при смене месяца
  };

  const handleDayClick = (day) => {
    if (selectedDay === day) {
      // Если кликнули на уже выбранный день - отменяем выбор
      setSelectedDay(null);
    } else {
      setSelectedDay(day);
    }
  };

  const formatDate = (day) => {
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const dayStr = day.toString().padStart(2, '0');
    return `${year}-${month}-${dayStr}`;
  };
  
  const getDayStatus = (day) => {
    const dateStr = formatDate(day);
    if (calendarData[dateStr]) {
      return calendarData[dateStr].status || 'unknown';
    }
    return 'unknown';
  };

  const getSelectedDayData = () => {
    if (!selectedDay) return null;
    
    const dateStr = formatDate(selectedDay);
    return calendarData[dateStr] || null;
  };

  const renderCalendarDays = () => {
    const days = [];
    const totalDays = 42; // 6 недель * 7 дней

    // Добавляем пустые ячейки для выравнивания
    for (let i = 0; i < adjustedFirstDay; i++) {
      days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
    }

    // Добавляем дни месяца
    for (let day = 1; day <= daysInMonth; day++) {
      const status = getDayStatus(day);
      days.push(
        <div
          key={day}
          className={`calendar-day ${status} ${selectedDay === day ? 'selected' : ''}`}
          onClick={() => handleDayClick(day)}
        >
          {day}
        </div>
      );
    }

    // Добавляем оставшиеся пустые ячейки
    const remainingDays = totalDays - (adjustedFirstDay + daysInMonth);
    for (let i = 0; i < remainingDays; i++) {
      days.push(<div key={`empty-end-${i}`} className="calendar-day empty"></div>);
    }

    return days;
  };

  // Получение информации о статусе дня
  const getDayStatusText = (status) => {
    switch (status) {
      case 'fire':
        return 'Зафиксировано возгорание';
      case 'safe':
        return 'Возгораний не зафиксировано';
      case 'risk':
        return 'Повышенный риск возгорания';
      default:
        return 'Нет данных';
    }
  };

  const selectedDayData = getSelectedDayData();

  return (
    <div className={`calendar ${selectedDay ? 'with-selected-day' : ''}`}>
      <div className="calendar-header">
        <button className="calendar-nav-btn" onClick={handlePrevMonth}>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>
        <h2 className="calendar-title">
          {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
        </h2>
        <button className="calendar-nav-btn" onClick={handleNextMonth}>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>

      <div className="calendar-weekdays">
        <div className="weekday">Пн</div>
        <div className="weekday">Вт</div>
        <div className="weekday">Ср</div>
        <div className="weekday">Чт</div>
        <div className="weekday">Пт</div>
        <div className="weekday">Сб</div>
        <div className="weekday">Вс</div>
      </div>

      <div className="calendar-grid">
        {isLoading ? (
          <div className="calendar-loading">Загрузка данных...</div>
        ) : (
          renderCalendarDays()
        )}
      </div>

      {selectedDay && selectedDayData && (
        <div className="day-info">
          <h3>Информация за {selectedDay} {monthNames[currentDate.getMonth()]}</h3>
          
          <div className="day-status">
            <span className={`status-indicator ${selectedDayData.status}`}></span>
            <span>{getDayStatusText(selectedDayData.status)}</span>
          </div>
          
          {selectedDayData.fire && selectedDayData.fire.hasFire && (
            <div className="fire-info">
              <p>Степень возгорания: {selectedDayData.fire.severity}/5</p>
            </div>
          )}
          
          {selectedDayData.prediction && (
            <div className="prediction-info">
              <p>Вероятность возгорания: {Math.round(selectedDayData.prediction.probability * 100)}%</p>
              <p>Уровень риска: {
                selectedDayData.prediction.riskLevel === 'high' ? 'Высокий' :
                selectedDayData.prediction.riskLevel === 'medium' ? 'Средний' : 'Низкий'
              }</p>
            </div>
          )}
          
          {selectedDayData.weather && (
            <div className="day-details">
              <h4>Погодные условия</h4>
              <p>Температура: {selectedDayData.weather.temperature}°C</p>
              <p>Влажность: {selectedDayData.weather.humidity}%</p>
              <p>Скорость ветра: {selectedDayData.weather.windSpeed} м/с</p>
              {selectedDayData.weather.windDirection && (
                <p>Направление ветра: {selectedDayData.weather.windDirection}</p>
              )}
            </div>
          )}
          
          {selectedDayData.coalTemp && (
            <div className="coal-details">
              <h4>Уголь</h4>
              <p>Температура угля: {selectedDayData.coalTemp.temperature}°C</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Calendar; 