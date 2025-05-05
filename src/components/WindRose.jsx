import { useState, useEffect } from 'react';
import { getWindData } from '../api';
import './WindRose.css';

const WindRose = () => {
  const [windData, setWindData] = useState({
    directions: [],
    averageSpeed: 0,
    maxSpeed: 0,
    dominantDirection: 'Неизвестно'
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadWindData();
  }, []);

  const loadWindData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await getWindData();
      
      if (response.success) {
        setWindData(response.data);
      } else {
        setError('Не удалось загрузить данные о ветре');
        console.error('Ошибка при загрузке данных о ветре:', response.message);
        
        // Используем запасные данные при ошибке
        setWindData({
          directions: [
            { wind_direction: 'С', count: 15 },
            { wind_direction: 'СВ', count: 25 },
            { wind_direction: 'В', count: 10 },
            { wind_direction: 'ЮВ', count: 5 },
            { wind_direction: 'Ю', count: 10 },
            { wind_direction: 'ЮЗ', count: 12 },
            { wind_direction: 'З', count: 18 },
            { wind_direction: 'СЗ', count: 14 }
          ],
          averageSpeed: 5.2,
          maxSpeed: 12,
          dominantDirection: 'СВ'
        });
      }
    } catch (err) {
      setError('Произошла ошибка при загрузке данных о ветре');
      console.error('Ошибка при загрузке данных о ветре:', err);
      
      // Используем запасные данные при ошибке
      setWindData({
        directions: [
          { wind_direction: 'С', count: 15 },
          { wind_direction: 'СВ', count: 25 },
          { wind_direction: 'В', count: 10 },
          { wind_direction: 'ЮВ', count: 5 },
          { wind_direction: 'Ю', count: 10 },
          { wind_direction: 'ЮЗ', count: 12 },
          { wind_direction: 'З', count: 18 },
          { wind_direction: 'СЗ', count: 14 }
        ],
        averageSpeed: 5.2,
        maxSpeed: 12,
        dominantDirection: 'СВ'
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Получаем максимальное количество наблюдений для нормализации
  const getMaxCount = () => {
    if (!windData.directions || windData.directions.length === 0) return 1;
    return Math.max(...windData.directions.map(dir => parseInt(dir.count)));
  };

  // Получаем позицию стрелки для преобладающего направления
  const getArrowRotation = () => {
    const directionMap = {
      'С': 0,
      'СВ': 45,
      'В': 90,
      'ЮВ': 135,
      'Ю': 180,
      'ЮЗ': 225,
      'З': 270,
      'СЗ': 315
    };
    
    return directionMap[windData.dominantDirection] || 0;
  };

  return (
    <div className="wind-rose">
      <h3>Роза ветров</h3>
      
      {isLoading ? (
        <div className="wind-loading">Загрузка данных о ветре...</div>
      ) : error ? (
        <div className="wind-error">{error}</div>
      ) : (
        <div className="wind-rose-content">
          <div className="compass">
            <div className="direction north">С</div>
            <div className="direction east">В</div>
            <div className="direction south">Ю</div>
            <div className="direction west">З</div>
            
            {windData.directions.map((dir, index) => {
              const directionMap = {
                'С': { angle: 0, label: 'С' },
                'СВ': { angle: 45, label: 'СВ' },
                'В': { angle: 90, label: 'В' },
                'ЮВ': { angle: 135, label: 'ЮВ' },
                'Ю': { angle: 180, label: 'Ю' },
                'ЮЗ': { angle: 225, label: 'ЮЗ' },
                'З': { angle: 270, label: 'З' },
                'СЗ': { angle: 315, label: 'СЗ' }
              };
              
              const dirInfo = directionMap[dir.wind_direction];
              if (!dirInfo) return null;
              
              const maxCount = getMaxCount();
              const length = 20 + (dir.count / maxCount) * 60; // От 20% до 80% радиуса
              
              const angle = dirInfo.angle * Math.PI / 180;
              const x = 50 + length * Math.sin(angle);
              const y = 50 - length * Math.cos(angle);
              
              return (
                <div 
                  key={index}
                  className="direction-line"
                  style={{
                    width: `${length}%`,
                    transform: `rotate(${dirInfo.angle}deg)`,
                    opacity: 0.7
                  }}
                  title={`${dir.wind_direction}: ${dir.count} наблюдений`}
                />
              );
            })}
            
            <div 
              className="compass-arrow"
              style={{ transform: `rotate(${getArrowRotation()}deg)` }}
            />
          </div>
          
          <div className="wind-stats">
            <p>Преобладающее направление: {windData.dominantDirection}</p>
            <p>Средняя скорость: {windData.averageSpeed} м/с</p>
            <p>Максимальная скорость: {windData.maxSpeed} м/с</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default WindRose; 