// Базовый URL для API
const API_URL = 'http://localhost:5000/api';

/**
 * Загрузка файла с данными о температуре угля
 * @param {File} file - CSV файл с данными о температуре угля
 * @returns {Promise}
 */
export const uploadCoalTemperature = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_URL}/upload/coal`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
};

/**
 * Загрузка файла с погодными данными
 * @param {File} file - CSV файл с погодными данными
 * @returns {Promise}
 */
export const uploadWeatherData = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_URL}/upload/weather`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
};

/**
 * Загрузка файла с историей возгораний
 * @param {File} file - CSV файл с историей возгораний
 * @returns {Promise}
 */
export const uploadFireHistory = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_URL}/upload/fire_history`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
};

/**
 * Запуск модели прогнозирования
 * @returns {Promise}
 */
export const generatePredictions = async () => {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
};

/**
 * Получение данных для календаря
 * @param {number} year - Год
 * @param {number} month - Месяц (1-12)
 * @returns {Promise}
 */
export const getCalendarData = async (year, month) => {
  const response = await fetch(`${API_URL}/calendar/${year}/${month}`);
  return response.json();
};

/**
 * Получение данных для карты
 * @returns {Promise}
 */
export const getMapData = async () => {
  const response = await fetch(`${API_URL}/map`);
  return response.json();
};

/**
 * Получение статистики
 * @returns {Promise}
 */
export const getStatistics = async () => {
  const response = await fetch(`${API_URL}/statistics`);
  return response.json();
};

/**
 * Получение данных о розе ветров
 * @returns {Promise}
 */
export const getWindData = async () => {
  const response = await fetch(`${API_URL}/wind`);
  return response.json();
};

// Экспортируем все функции API в одном объекте
export default {
  uploadCoalTemperature,
  uploadWeatherData,
  uploadFireHistory,
  generatePredictions,
  getCalendarData,
  getMapData,
  getStatistics,
  getWindData
}; 