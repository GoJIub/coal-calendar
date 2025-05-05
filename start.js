import { spawn } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'

// Получаем текущую директорию
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Путь к директории сервера
const serverDir = path.join(__dirname, 'server');

// Запуск бэкенда
console.log('Запуск бэкенда...');
const serverProcess = spawn('npm', ['run', 'dev'], {
  cwd: serverDir,
  stdio: 'inherit',
  shell: true
});

// Запуск фронтенда
console.log('Запуск фронтенда...');
const clientProcess = spawn('npm', ['run', 'dev'], {
  cwd: __dirname,
  stdio: 'inherit',
  shell: true
});

// Обработка завершения процессов
process.on('SIGINT', () => {
  console.log('Завершение работы...');
  serverProcess.kill();
  clientProcess.kill();
  process.exit();
});

process.on('exit', () => {
  serverProcess.kill();
  clientProcess.kill();
}); 