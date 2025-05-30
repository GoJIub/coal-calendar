import { useState, useEffect } from 'react';
import { getStatistics } from '../api';
import './Statistics.css';

const Statistics = () => {
  const [stats, setStats] = useState({
    totalFires: 0,
    daysSinceLastFire: 0,
    averageTemperature: 0,
    currentRiskLevel: 'Неизвестно',
    fireDetails: [] // New field for detailed fire history
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await getStatistics();
      
      if (response.success) {
        setStats({
          totalFires: response.data.totalFires,
          daysSinceLastFire: response.data.daysSinceLastFire,
          averageTemperature: response.data.averageTemperature,
          currentRiskLevel: response.data.currentRiskLevel,
          fireDetails: response.data.fireDetails // Populate detailed fire history
        });
      } else {
        setError('Не удалось загрузить статистику');
        console.error('Ошибка при загрузке статистики:', response.message);
        
        // Используем запасные данные при ошибке
        setStats({
          totalFires: 42,
          daysSinceLastFire: 14,
          averageTemperature: 27,
          currentRiskLevel: 'Средний',
          fireDetails: [] // Empty fire details as fallback
        });
      }
    } catch (err) {
      setError('Произошла ошибка при загрузке статистики');
      console.error('Ошибка при загрузке статистики:', err);
      
      // Используем запасные данные при ошибке
      setStats({
        totalFires: 42,
        daysSinceLastFire: 14,
        averageTemperature: 27,
        currentRiskLevel: 'Средний',
        fireDetails: [] // Empty fire details as fallback
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskLevelClass = (level) => {
    switch (level.toLowerCase()) {
      case 'высокий':
      case 'high':
        return 'high-risk';
      case 'средний':
      case 'medium':
        return 'medium-risk';
      case 'низкий':
      case 'low':
        return 'low-risk';
      default:
        return '';
    }
  };

  const formatRiskLevel = (level) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'Высокий';
      case 'medium':
        return 'Средний';
      case 'low':
        return 'Низкий';
      default:
        return level;
    }
  };

  return (
    <div className="statistics">
      <h3>Статистика возгораний</h3>
      
      {isLoading ? (
        <div className="stats-loading">Загрузка статистики...</div>
      ) : error ? (
        <div className="stats-error">{error}</div>
      ) : (
        <div className="stats-content">
          <div className="stat-item">
            <div className="stat-label">Всего пожаров</div>
            <div className="stat-value">{stats.totalFires}</div>
          </div>
          
          <div className="stat-item">
            <div className="stat-label">Риск возгорания</div>
            <div className={`stat-value ${getRiskLevelClass(stats.currentRiskLevel)}`}>
              {formatRiskLevel(stats.currentRiskLevel)}
            </div>
          </div>
          
          <div className="stat-item">
            <div className="stat-label">Дней без пожаров</div>
            <div className="stat-value">{stats.daysSinceLastFire}</div>
          </div>
          
          <div className="stat-item">
            <div className="stat-label">Средняя температура</div>
            <div className="stat-value">{stats.averageTemperature}°C</div>
          </div>

          <div className="stat-item">
            <div className="stat-label">Детали пожаров</div>
            <ul>
              {stats.fireDetails.map((fire, index) => (
                <li key={index}>
                  {`Дата: ${fire.creation_date}, Груз: ${fire.cargo}, Вес: ${fire.weight}, Склад: ${fire.warehouse}`}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Statistics;