import { useState } from 'react';
import { uploadCoalTemperature, uploadWeatherData, uploadFireHistory, generatePredictions } from '../api';
import './UploadModal.css';

const UploadModal = ({ onClose }) => {
  const [coalFile, setCoalFile] = useState(null);
  const [weatherFile, setWeatherFile] = useState(null);
  const [fireHistoryFile, setFireHistoryFile] = useState(null);
  const [isDragging, setIsDragging] = useState({ coal: false, weather: false, fire: false });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const validateFile = (file) => {
    if (!file) return false;
    
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      setError('Пожалуйста, выберите файл в формате CSV');
      return false;
    }
    
    return true;
  };

  const handleCoalFileChange = (event) => {
    const file = event.target.files[0];
    if (validateFile(file)) {
      setCoalFile(file);
      setError(null);
    }
  };

  const handleWeatherFileChange = (event) => {
    const file = event.target.files[0];
    if (validateFile(file)) {
      setWeatherFile(file);
      setError(null);
    }
  };

  const handleFireHistoryFileChange = (event) => {
    const file = event.target.files[0];
    if (validateFile(file)) {
      setFireHistoryFile(file);
      setError(null);
    }
  };

  const handleDragOver = (e, type) => {
    e.preventDefault();
    setIsDragging(prev => ({ ...prev, [type]: true }));
  };

  const handleDragLeave = (e, type) => {
    e.preventDefault();
    setIsDragging(prev => ({ ...prev, [type]: false }));
  };

  const handleDrop = (e, type) => {
    e.preventDefault();
    setIsDragging(prev => ({ ...prev, [type]: false }));
    
    const file = e.dataTransfer.files[0];
    if (!validateFile(file)) return;
    
    if (type === 'coal') setCoalFile(file);
    else if (type === 'weather') setWeatherFile(file);
    else if (type === 'fire') setFireHistoryFile(file);
    
    setError(null);
  };

  const uploadFiles = async () => {
    if (!coalFile && !weatherFile && !fireHistoryFile) {
      setError('Пожалуйста, выберите хотя бы один файл для загрузки');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      // Загрузка файлов
      const uploadPromises = [];
      
      if (coalFile) {
        uploadPromises.push(uploadCoalTemperature(coalFile));
      }
      
      if (weatherFile) {
        uploadPromises.push(uploadWeatherData(weatherFile));
      }
      
      if (fireHistoryFile) {
        uploadPromises.push(uploadFireHistory(fireHistoryFile));
      }
      
      const results = await Promise.all(uploadPromises);
      
      // Проверяем результаты загрузки
      const hasError = results.some(result => !result.success);
      
      if (hasError) {
        const errorMessages = results
          .filter(result => !result.success)
          .map(result => result.message)
          .join(', ');
        
        setError(`Ошибка при загрузке файлов: ${errorMessages}`);
      } else {
        setSuccess('Файлы успешно загружены');
        
        // Запускаем модель прогнозирования
        try {
          const predictionResult = await generatePredictions();
          
          if (predictionResult.success) {
            setSuccess('Файлы успешно загружены и прогнозы созданы');
          } else {
            setError('Файлы загружены, но произошла ошибка при создании прогнозов');
          }
        } catch (predError) {
          console.error('Ошибка при запуске модели прогнозирования:', predError);
          setError('Файлы загружены, но произошла ошибка при создании прогнозов');
        }
      }
    } catch (err) {
      console.error('Ошибка при загрузке файлов:', err);
      setError('Произошла ошибка при загрузке файлов. Пожалуйста, попробуйте снова.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="upload-modal-overlay">
      <div className="upload-modal">
        <h2>Загрузка данных</h2>
        
        <div className="upload-sections">
          <div className="upload-section">
            <h3>Температура угля</h3>
            <div 
              className={`file-upload-area ${isDragging.coal ? 'dragging' : ''} ${coalFile ? 'has-file' : ''}`}
              onDragOver={(e) => handleDragOver(e, 'coal')}
              onDragLeave={(e) => handleDragLeave(e, 'coal')}
              onDrop={(e) => handleDrop(e, 'coal')}
            >
              {coalFile ? (
                <div className="file-info">
                  <span className="file-name">{coalFile.name}</span>
                  <button 
                    className="remove-file-btn"
                    onClick={() => setCoalFile(null)}
                  >
                    ✕
                  </button>
                </div>
              ) : (
                <>
                  <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M14 3V7C14 7.26522 14.1054 7.51957 14.2929 7.70711C14.4804 7.89464 14.7348 8 15 8H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 8V5C5 4.46957 5.21071 3.96086 5.58579 3.58579C5.96086 3.21071 6.46957 3 7 3H14L19 8V19C19 19.5304 18.7893 20.0391 18.4142 20.4142C18.0391 20.7893 17.5304 21 17 21H7C6.46957 21 5.96086 20.7893 5.58579 20.4142C5.21071 20.0391 5 19.5304 5 19V16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 15L9 12M9 12L6 15M9 12V18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Перетащите файл или <label className="file-label">выберите файл<input type="file" accept=".csv" onChange={handleCoalFileChange} /></label></span>
                </>
              )}
            </div>
          </div>
          
          <div className="upload-section">
            <h3>Погодные данные</h3>
            <div 
              className={`file-upload-area ${isDragging.weather ? 'dragging' : ''} ${weatherFile ? 'has-file' : ''}`}
              onDragOver={(e) => handleDragOver(e, 'weather')}
              onDragLeave={(e) => handleDragLeave(e, 'weather')}
              onDrop={(e) => handleDrop(e, 'weather')}
            >
              {weatherFile ? (
                <div className="file-info">
                  <span className="file-name">{weatherFile.name}</span>
                  <button 
                    className="remove-file-btn"
                    onClick={() => setWeatherFile(null)}
                  >
                    ✕
                  </button>
                </div>
              ) : (
                <>
                  <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M14 3V7C14 7.26522 14.1054 7.51957 14.2929 7.70711C14.4804 7.89464 14.7348 8 15 8H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 8V5C5 4.46957 5.21071 3.96086 5.58579 3.58579C5.96086 3.21071 6.46957 3 7 3H14L19 8V19C19 19.5304 18.7893 20.0391 18.4142 20.4142C18.0391 20.7893 17.5304 21 17 21H7C6.46957 21 5.96086 20.7893 5.58579 20.4142C5.21071 20.0391 5 19.5304 5 19V16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 15L9 12M9 12L6 15M9 12V18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Перетащите файл или <label className="file-label">выберите файл<input type="file" accept=".csv" onChange={handleWeatherFileChange} /></label></span>
                </>
              )}
            </div>
          </div>
          
          <div className="upload-section">
            <h3>История возгораний</h3>
            <div 
              className={`file-upload-area ${isDragging.fire ? 'dragging' : ''} ${fireHistoryFile ? 'has-file' : ''}`}
              onDragOver={(e) => handleDragOver(e, 'fire')}
              onDragLeave={(e) => handleDragLeave(e, 'fire')}
              onDrop={(e) => handleDrop(e, 'fire')}
            >
              {fireHistoryFile ? (
                <div className="file-info">
                  <span className="file-name">{fireHistoryFile.name}</span>
                  <button 
                    className="remove-file-btn"
                    onClick={() => setFireHistoryFile(null)}
                  >
                    ✕
                  </button>
                </div>
              ) : (
                <>
                  <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M14 3V7C14 7.26522 14.1054 7.51957 14.2929 7.70711C14.4804 7.89464 14.7348 8 15 8H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 8V5C5 4.46957 5.21071 3.96086 5.58579 3.58579C5.96086 3.21071 6.46957 3 7 3H14L19 8V19C19 19.5304 18.7893 20.0391 18.4142 20.4142C18.0391 20.7893 17.5304 21 17 21H7C6.46957 21 5.96086 20.7893 5.58579 20.4142C5.21071 20.0391 5 19.5304 5 19V16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 15L9 12M9 12L6 15M9 12V18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Перетащите файл или <label className="file-label">выберите файл<input type="file" accept=".csv" onChange={handleFireHistoryFileChange} /></label></span>
                </>
              )}
            </div>
          </div>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        
        <div className="modal-actions">
          <button className="modal-cancel-btn" onClick={onClose}>Отмена</button>
          <button 
            className="modal-upload-btn" 
            onClick={uploadFiles}
            disabled={isLoading}
          >
            {isLoading ? 'Загрузка...' : 'Загрузить и создать прогнозы'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadModal; 