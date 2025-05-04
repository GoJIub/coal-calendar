<template>
  <div class="main-wrapper">
    <header class="main-header">
      <h1 class="main-title">Предсказание возгораний</h1>
      <div class="header-actions">
        <button class="header-btn" @click="showUploadModal = true">
          <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>
          Добавить
        </button>
        <button class="header-btn theme-toggle" @click="toggleTheme">
          <img :src="themeIcon" alt="Тема" width="30" height="30" />
        </button>
      </div>
    </header>
    <main class="main-content">
      <div class="center-area">
        <div class="side-buttons-mockup">
          <button class="side-btn-mockup">
            <svg width="59" height="59" viewBox="0 0 59 59" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M58.3252 0.416035C58.5363 0.589111 58.7063 0.806906 58.823 1.0537C58.9397 1.30048 59.0002 1.57011 59 1.8431V53.4681C58.9997 53.8942 58.8519 54.307 58.5817 54.6364C58.3114 54.9658 57.9354 55.1915 57.5176 55.275L39.0801 58.9625C38.8416 59.0102 38.5959 59.0102 38.3574 58.9625L20.2812 55.3487L2.20512 58.9625C1.93774 59.0159 1.66183 59.0094 1.39727 58.9434C1.13271 58.8773 0.886091 58.7534 0.675179 58.5806C0.464266 58.4078 0.294312 58.1903 0.17756 57.9439C0.0608075 57.6975 0.000164657 57.4283 0 57.1556L0 5.5306C0.000257321 5.10452 0.148076 4.69168 0.418323 4.36228C0.688569 4.03287 1.06456 3.80723 1.48238 3.72372L19.9199 0.0362227C20.1584 -0.0114594 20.4041 -0.0114594 20.6426 0.0362227L38.7188 3.64997L56.7949 0.0362227C57.0622 -0.0175565 57.3381 -0.0113854 57.6027 0.0542914C57.8673 0.119968 58.1141 0.243516 58.3252 0.416035ZM36.875 7.04247L22.125 4.09247V51.9562L36.875 54.9062V7.04247ZM40.5625 54.9062L55.3125 51.9562V4.09247L40.5625 7.04247V54.9062ZM18.4375 51.9562V4.09247L3.6875 7.04247V54.9062L18.4375 51.9562Z" fill="currentColor"/>
            </svg>
          </button>
          <button class="side-btn-mockup">
            <svg width="70" height="70" viewBox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g>
                <path d="M34.9999 40.8334C36.547 40.8334 38.0307 40.2188 39.1247 39.1249C40.2187 38.0309 40.8332 36.5472 40.8332 35.0001C40.8332 33.453 40.2187 31.9693 39.1247 30.8753C38.0307 29.7813 36.547 29.1667 34.9999 29.1667C33.4528 29.1667 31.9691 29.7813 30.8751 30.8753C29.7812 31.9693 29.1666 33.453 29.1666 35.0001C29.1666 36.5472 29.7812 38.0309 30.8751 39.1249C31.9691 40.2188 33.4528 40.8334 34.9999 40.8334Z" stroke="currentColor" stroke-width="2.81713" stroke-miterlimit="10"/>
                <path d="M20.4167 34.9994H2.91667M67.0833 34.9994H49.5833M35 49.5828V67.0828M45.3133 45.3128L49.4375 49.4369M20.5625 20.5619L24.6896 24.6861M45.3133 24.6861L49.4375 20.5619M20.5625 49.4369L24.6896 45.3128M35 2.91611V20.4161" stroke="currentColor" stroke-width="2.81713" stroke-miterlimit="10" stroke-linecap="round"/>
              </g>
            </svg>
          </button>
          <button class="side-btn-mockup">
            <svg width="58" height="58" viewBox="0 0 58 58" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g>
                <path fill-rule="evenodd" clip-rule="evenodd" d="M0 0H3.625V54.375H58V58H0V0ZM53.7116 11.2846C53.896 11.4355 54.0488 11.6211 54.1613 11.8311C54.2738 12.041 54.3439 12.271 54.3674 12.508C54.391 12.745 54.3676 12.9844 54.2986 13.2123C54.2296 13.4403 54.1164 13.6524 53.9654 13.8366L37.6529 33.7741C37.4925 33.9698 37.293 34.1298 37.0671 34.2437C36.8413 34.3577 36.594 34.4231 36.3414 34.4357C36.0887 34.4483 35.8362 34.4079 35.6 34.3171C35.3639 34.2262 35.1494 34.087 34.9704 33.9082L25.5925 24.5304L12.3395 42.7533C12.0496 43.1219 11.6281 43.3638 11.1635 43.4282C10.6989 43.4925 10.2275 43.3743 9.8483 43.0983C9.46908 42.8224 9.2116 42.4102 9.12996 41.9483C9.04832 41.4865 9.14888 41.011 9.4105 40.6217L23.9105 20.6842C24.0644 20.4722 24.2624 20.2961 24.491 20.168C24.7195 20.0399 24.9731 19.9629 25.2342 19.9422C25.4954 19.9215 25.758 19.9577 26.0038 20.0483C26.2496 20.1388 26.4729 20.2816 26.6583 20.4667L36.1159 29.928L51.1596 11.5384C51.3105 11.354 51.4961 11.2012 51.7061 11.0887C51.916 10.9762 52.146 10.9061 52.383 10.8826C52.62 10.859 52.8594 10.8824 53.0873 10.9514C53.3153 11.0204 53.5275 11.1336 53.7116 11.2846Z" fill="currentColor"/>
              </g>
            </svg>
          </button>
        </div>
        <div class="center-window"></div>
      </div>
    </main>
    <footer class="footer">
      <nav class="footer-nav">
        <div class="footer-nav-item">
          <a href="#" @click.prevent="toggleMenu('contacts')">Контакты</a>
          <div v-if="activeMenu === 'contacts'" class="context-menu menu-align-left">
            <div class="context-menu-item">Email: berezin.aw06@gmail.com</div>
            <div class="context-menu-item">Телефон: +7 (985) 215-47-85</div>
            <div class="context-menu-item">Git: https://github.com/hxllmvdx/MatMod-glowbyte-case.git</div>
          </div>
        </div>
        <div class="footer-nav-item">
          <a href="#" @click.prevent="showQrModal = true">О нас</a>
        </div>
        <div class="footer-nav-item">
          <a href="#" @click.prevent="showInstructionModal = true">Инструкция</a>
          <div v-if="activeMenu === 'instructions'" class="context-menu">
            <div class="context-menu-item">Начало работы</div>
            <div class="context-menu-item">Основные функции</div>
          </div>
        </div>
      </nav>
      <div class="footer-logo-copyright">
        <img src="./assets/glowbyte.svg" alt="GlowByte Logo" class="glowbyte-logo" />
        <span>© Copyright</span>
      </div>
    </footer>

    <!-- Модальное окно загрузки -->
    <div v-if="showUploadModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Загрузка файла</h2>
          <button class="modal-close" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="upload-area" 
               @dragover.prevent="handleDragOver"
               @dragleave.prevent="handleDragLeave"
               @drop.prevent="handleDrop"
               :class="{ 'drag-over': isDragging }">
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileSelect" 
              accept=".csv"
              class="file-input"
            >
            <div class="upload-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
            </div>
            <p class="upload-text">Перетащите CSV файл сюда или кликните для выбора</p>
            <p class="upload-hint">Поддерживаются только файлы формата .csv</p>
          </div>
          <div v-if="selectedFile" class="selected-file">
            <p>Выбран файл: {{ selectedFile.name }}</p>
            <button class="upload-btn" @click="uploadFile">Загрузить</button>
          </div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно с QR-кодами -->
    <div v-if="showQrModal" class="modal-overlay" @click="closeQrModal">
      <div class="modal-content qr-modal" @click.stop>
        <div class="modal-header">
          <h2>Наши QR-коды</h2>
          <button class="modal-close" @click="closeQrModal">×</button>
        </div>
        <div class="modal-body qr-list">
          <div class="qr-item" v-for="(qr, idx) in qrCodes" :key="idx">
            <img :src="qr.src" :alt="qr.caption" class="qr-img" />
            <div class="qr-caption">{{ qr.caption }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно инструкции -->
    <div v-if="showInstructionModal" class="modal-overlay" @click="closeInstructionModal">
      <div class="modal-content instruction-modal" @click.stop>
        <div class="modal-header">
          <h2>Краткая инструкция</h2>
          <button class="modal-close" @click="closeInstructionModal">×</button>
        </div>
        <div class="modal-body instruction-body">
          <div v-html="instructionHtml"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SunIcon from './assets/sun.svg';
import MoonIcon from './assets/moon.svg';
import { marked } from 'marked';

const instructionMd = `- **Интерфейс**:
  - Шапка: "Добавить", переключение темы (солнце/луна).
  - Боковая панель: Карта, роза ветров, статистика.
  - Основное: Календарь (красный — возгорание, зелёный — нет, жёлтый — риск).
  - Подвал: Контакты, "О нас", инструкция.
- **Функции**:
  1. **Добавить данные**: "Добавить" → файлы/ввод → подтвердить.
  2. **Календарь**: Стрелки для месяцев, клик на день для инфо.
  3. **Дополнительные функции**: Переключение через боковую панель.`;

export default {
  data() {
    return {
      isDarkTheme: false,
      activeMenu: null,
      showUploadModal: false,
      selectedFile: null,
      isDragging: false,
      errorMessage: '',
      showQrModal: false,
      showInstructionModal: false,
      qrCodes: [
        { src: 'https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://youtube.com/', caption: 'YouTube' },
        { src: 'https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://vk.com/', caption: 'VK' },
        { src: 'https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://t.me/', caption: 'Telegram' },
        { src: 'https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://github.com/', caption: 'GitHub' },
        { src: 'https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://example.com/', caption: 'Example' }
      ]
    }
  },
  computed: {
    themeIcon() {
      return this.isDarkTheme ? SunIcon : MoonIcon;
    },
    instructionHtml() {
      return marked.parse(instructionMd);
    }
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      if (this.isDarkTheme) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    },
    toggleMenu(menuName) {
      if (this.activeMenu === menuName) {
        this.activeMenu = null;
      } else {
        this.activeMenu = menuName;
        // Проверяем позицию меню после его отображения
        this.$nextTick(() => {
          const menu = document.querySelector('.context-menu');
          if (menu) {
            const rect = menu.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            this.isMenuLeft = rect.right > viewportWidth;
          }
        });
      }
    },
    closeModal() {
      this.showUploadModal = false;
      this.selectedFile = null;
      this.errorMessage = '';
      this.isDragging = false;
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      this.validateAndSetFile(file);
    },
    handleDragOver() {
      this.isDragging = true;
    },
    handleDragLeave() {
      this.isDragging = false;
    },
    handleDrop(event) {
      this.isDragging = false;
      const file = event.dataTransfer.files[0];
      this.validateAndSetFile(file);
    },
    validateAndSetFile(file) {
      if (!file) return;
      
      if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
        this.errorMessage = 'Пожалуйста, выберите файл в формате CSV';
        this.selectedFile = null;
        return;
      }

      this.errorMessage = '';
      this.selectedFile = file;
    },
    uploadFile() {
      if (!this.selectedFile) return;
      
      // Здесь будет логика загрузки файла
      console.log('Загрузка файла:', this.selectedFile.name);
      
      // После успешной загрузки
      this.closeModal();
    },
    closeQrModal() {
      this.showQrModal = false;
    },
    closeInstructionModal() {
      this.showInstructionModal = false;
    }
  },
  mounted() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      this.isDarkTheme = true;
      document.documentElement.classList.add('dark');
    }

    // Закрытие меню при клике вне его
    document.addEventListener('click', (event) => {
      if (!event.target.closest('.footer-nav-item')) {
        this.activeMenu = null;
      }
    });
  }
};
</script>

<style>
  .main-wrapper {
    min-height: 100vh;
    background: var(--main-bg);
    color: var(--main-text);
    display: flex;
    flex-direction: column;
    font-family: 'Russo One', sans-serif;
  }
  .main-title {
    font-family: 'Russo One', sans-serif;
  }
  .main-content {
    flex: 1 0 auto;
  }
  .footer {
    flex-shrink: 0;
  }

  .footer-nav-item {
    position: relative;
  }

  .footer-logo-copyright {
    display: flex;
    align-items: center;
    gap: 0.7rem;
  }

  .context-menu {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--main-header-footer);
    border: 1px solid var(--main-border);
    border-radius: 8px;
    padding: 0.5rem 0;
    min-width: 200px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    margin-bottom: 0.5rem;
  }

  .context-menu.menu-align-left {
    left: 0;
    transform: none;
  }

  .context-menu.menu-align-left::after {
    left: 24px;
    transform: none;
  }

  .context-menu-item {
    padding: 0.5rem 1rem;
    color: var(--main-header-footer-text);
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .context-menu-item:hover {
    background-color: var(--main-border);
  }

  @media (max-width: 900px) {
    .context-menu {
      position: fixed;
      bottom: auto;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      margin: 0;
      max-width: 90%;
    }

    .context-menu.menu-left {
      left: 50%;
      right: auto;
      transform: translate(-50%, -50%);
    }

    .context-menu::after {
      display: none;
    }
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    background: var(--main-bg);
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--main-border);
  }

  .modal-header h2 {
    margin: 0;
    color: var(--main-text);
    font-size: 1.5rem;
  }

  .modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: var(--main-text);
    cursor: pointer;
    padding: 0.5rem;
    line-height: 1;
  }

  .modal-body {
    padding: 1.5rem;
  }

  .upload-area {
    border: 2px dashed var(--main-border);
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .upload-area.drag-over {
    border-color: #007aff;
    background: rgba(0, 122, 255, 0.1);
  }

  .file-input {
    display: none;
  }

  .upload-icon {
    color: var(--main-text);
    margin-bottom: 1rem;
  }

  .upload-text {
    margin: 0 0 0.5rem;
    color: var(--main-text);
    font-size: 1.1rem;
  }

  .upload-hint {
    margin: 0;
    color: var(--main-text);
    opacity: 0.7;
    font-size: 0.9rem;
  }

  .selected-file {
    margin-top: 1rem;
    padding: 1rem;
    background: var(--main-header-footer);
    border-radius: 8px;
    text-align: center;
  }

  .upload-btn {
    background: #007aff;
    color: white;
    border: none;
    padding: 0.5rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    margin-top: 1rem;
    transition: background-color 0.3s;
  }

  .upload-btn:hover {
    background: #0056b3;
  }

  .error-message {
    color: #dc3545;
    margin-top: 1rem;
    text-align: center;
  }

  .qr-modal {
    max-width: 800px;
  }
  .qr-list {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    justify-content: center;
    align-items: center;
    padding: 2rem 1rem;
  }
  .qr-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    min-width: 120px;
  }
  .qr-img {
    width: 120px;
    height: 120px;
    border-radius: 12px;
    background: #fff;
    border: 1px solid var(--main-border);
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  }
  .qr-caption {
    color: var(--main-text);
    font-size: 1rem;
    text-align: center;
    margin-top: 0.5rem;
    font-weight: 500;
  }
  .glowbyte-logo {
    height: 70px;
    width: 70px;
    margin: 0;
    padding: 0;
    display: block;
    background: transparent;
    overflow: hidden;
    vertical-align: middle;
    object-fit: contain;
  }
  .main-header {
    gap: 1.5rem;
  }
  .instruction-modal {
    max-width: 600px;
  }
  .instruction-body {
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--main-text);
    padding: 1.5rem;
  }
  .instruction-body ul {
    margin-left: 1.2em;
    margin-bottom: 1em;
  }
  .instruction-body ol {
    margin-left: 1.5em;
    margin-bottom: 1em;
  }
  .instruction-body strong, .instruction-body b {
    font-weight: bold;
  }
</style>