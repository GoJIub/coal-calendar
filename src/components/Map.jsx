import { useState, useEffect } from 'react';
import { getMapData } from '../api';
import './Map.css';

const Map = () => {
  const [mapData, setMapData] = useState(null);
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadMapData();
  }, []);

  const loadMapData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await getMapData();
      
      if (response.success) {
        setMapData({
          points: response.data.map(location => ({
            id: location.location,
            x: location.coordinates.x,
            y: location.coordinates.y,
            location: location.location,
            status: getLocationStatus(location),
            fire: location.fire,
            prediction: location.prediction,
            weather: location.weather
          }))
        });
      } else {
        setError('Не удалось загрузить данные карты');
        console.error('Ошибка при загрузке данных карты:', response.message);
        
        // Используем запасные данные при ошибке
        setMapData(getFallbackData());
      }
    } catch (err) {
      setError('Произошла ошибка при загрузке данных карты');
      console.error('Ошибка при загрузке данных карты:', err);
      
      // Используем запасные данные при ошибке
      setMapData(getFallbackData());
    } finally {
      setIsLoading(false);
    }
  };

  // Определение статуса локации на основе данных о пожарах и прогнозах
  const getLocationStatus = (location) => {
    if (location.fire && location.fire.has_fire) {
      return 'fire';
    } else if (location.prediction && location.prediction.risk_level === 'high') {
      return 'risk';
    } else {
      return 'safe';
    }
  };

  // Запасные данные, если API недоступен
  const getFallbackData = () => {
    return {
      points: [
        { id: 1, x: 30, y: 40, location: 'Зона A', status: 'fire', temperature: 35, humidity: 30, windSpeed: 8 },
        { id: 2, x: 60, y: 70, location: 'Зона B', status: 'safe', temperature: 25, humidity: 45, windSpeed: 5 },
        { id: 3, x: 80, y: 20, location: 'Зона C', status: 'risk', temperature: 30, humidity: 35, windSpeed: 12 },
      ]
    };
  };

  const handlePointClick = (point) => {
    if (selectedPoint && selectedPoint.id === point.id) {
      // If clicking on the same point, deselect it
      setSelectedPoint(null);
    } else {
      // Otherwise, select the new point
      setSelectedPoint(point);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'fire':
        return '#ff0000';
      case 'safe':
        return '#00ff00';
      case 'risk':
        return '#ffff00';
      default:
        return '#808080';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'fire':
        return 'Зафиксировано возгорание';
      case 'safe':
        return 'Возгораний не зафиксировано';
      case 'risk':
        return 'Повышенный риск возгорания';
      default:
        return 'Статус неизвестен';
    }
  };

  return (
    <div className="map-container">
      {isLoading ? (
        <div className="map-loading">Загрузка карты...</div>
      ) : error ? (
        <div className="map-error">{error}</div>
      ) : (
        <>
          <div className="map">
            {mapData?.points.map((point) => (
              <div
                key={point.id}
                className="map-point"
                style={{
                  left: `${point.x}%`,
                  top: `${point.y}%`,
                  backgroundColor: getStatusColor(point.status)
                }}
                onClick={() => handlePointClick(point)}
              >
                <span className="point-tooltip">{point.location}</span>
              </div>
            ))}
          </div>

          {selectedPoint && (
            <div className="point-info">
              <h3>Информация о точке: {selectedPoint.location}</h3>
              <div className="point-status">
                <span
                  className="status-indicator"
                  style={{ backgroundColor: getStatusColor(selectedPoint.status) }}
                />
                <span>{getStatusText(selectedPoint.status)}</span>
              </div>
              
              {selectedPoint.fire && (
                <div className="fire-details">
                  <h4>Данные о возгорании</h4>
                  {selectedPoint.fire.has_fire ? (
                    <p>Степень возгорания: {selectedPoint.fire.severity}/5</p>
                  ) : (
                    <p>Возгораний не зафиксировано</p>
                  )}
                </div>
              )}
              
              {selectedPoint.prediction && (
                <div className="prediction-details">
                  <h4>Прогноз</h4>
                  <p>Вероятность возгорания: {Math.round(selectedPoint.prediction.fire_probability * 100)}%</p>
                  <p>Уровень риска: {
                    selectedPoint.prediction.risk_level === 'high' ? 'Высокий' :
                    selectedPoint.prediction.risk_level === 'medium' ? 'Средний' : 'Низкий'
                  }</p>
                </div>
              )}
              
              {selectedPoint.weather && (
                <div className="point-details">
                  <h4>Погодные условия</h4>
                  <p>Температура: {selectedPoint.weather.temperature}°C</p>
                  <p>Влажность: {selectedPoint.weather.humidity}%</p>
                  <p>Скорость ветра: {selectedPoint.weather.wind_speed} м/с</p>
                  {selectedPoint.weather.wind_direction && (
                    <p>Направление ветра: {selectedPoint.weather.wind_direction}</p>
                  )}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Map; 