<div align="center">

# ⚡ Custom Discord Rich Presence (RPC)

**Ultimate Animated & Customizable Discord Rich Presence with Tray Control Panel & Multi-Language Support (EN / RU)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Presence-5865F2?logo=discord&logoColor=white)](https://discord.com)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org/)
[![Language](https://img.shields.io/badge/Language-English%20%7C%20%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-purple)](#)

[English Documentation](#-english-guide) • [Русская документация](#-инструкция-на-русском)

</div>

---

## 🔍 Tags & Topics (Keywords)
`antigravity-rpc` `antigravity-discordrpc` `discord-rpc` `custom-discord-rpc` `animated-discord-rpc` `discord-rich-presence` `rich-presence` `discord-status` `multi-language` `tray-app` `discord-presence-customizer` `custom-status` `fameboyq`

---

## 🌟 Features / Возможности

* 🔄 **Animated Frame Rotation:** Cycles through customizable status lines every few seconds smoothly without Discord rate limits.
* 🌐 **Multi-Language Support (EN / RU):** Switch between English and Russian with 1 click in the tray menu or GUI.
* 🖥️ **System Tray Control Panel:** Modern dark-mode GUI control panel running in your Windows tray bar.
* 🔗 **Custom Profile Buttons:** Add up to 2 clickable buttons linking to your website, Telegram, GitHub, or social profiles.
* 🛠️ **Fully Configurable:** Change Client ID, animation interval, image keys, states, and text lines inside `config.json` or live through the UI.
* 🚀 **1-Click Setup:** Includes ready-to-run `.bat` scripts for seamless installation and execution.

---

## 🇺🇸 English Guide

### 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Fameboyq/custom-discord-rpc.git
   cd custom-discord-rpc
   ```

2. **Install Dependencies:**
   * Double-click `install.bat`  
   * Or run via terminal:
     ```bash
     npm install
     pip install -r requirements.txt
     ```

3. **Launch:**
   * Double-click `start.bat`  
   * Or start manually:
     ```bash
     node index.js
     pythonw tray_app.py
     ```

### ⚙️ Configuration (`config.json`)

You can edit all settings via the Tray Control Panel or directly in `config.json`:

```json
{
  "client_id": "1440730997460172810",
  "language": "en",
  "interval_seconds": 6,
  "buttons": [
    { "label": "Website", "url": "https://fameboyq.fun" },
    { "label": "Telegram", "url": "https://t.me/fameboyq" }
  ]
}
```

* `client_id`: Your Discord Application ID (from the [Discord Developer Portal](https://discord.com/developers/applications)).
* `language`: Current language (`"en"` or `"ru"`).
* `interval_seconds`: Time between frame transitions (recommended: `6` or more to stay within Discord rate limits).
* `buttons`: Array of up to 2 clickable buttons with `label` and `url`.
* `presets`: Rotating status lines for both English and Russian.

---

## 🇷🇺 Инструкция на русском

### 🚀 Быстрый запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Fameboyq/custom-discord-rpc.git
   cd custom-discord-rpc
   ```

2. **Установите зависимости:**
   * Запустите файл `install.bat` в один клик.  
   * Либо через командную строку:
     ```bash
     npm install
     pip install -r requirements.txt
     ```

3. **Запуск:**
   * Запустите `start.bat`.
   * В системном трее появится иконка управления, а в профиле Discord — анимированный статус с кнопками.

### 🌐 Переключение языка
* **В приложении:** Откройте панель из трея и нажмите переключатель `[ EN | RU ]`.
* **В трее:** Правый клик по иконке в трее -> `Lang` -> выберите `English` или `Русский`.

---

## 🛠️ Discord Developer Portal (Кастомные иконки)

If you want to use your own Discord Application:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications) and create a **New Application**.
2. Copy your **Application ID** and paste it into `config.json` as `client_id`.
3. Under **Rich Presence -> Art Assets**, upload your logos and name them (e.g., `large_image`, `small_image`).
4. Update the names in `config.json`.

---

## 👤 Author

* **Fameboyq** - [GitHub Profile](https://github.com/Fameboyq) • [Website](https://fameboyq.fun) • [Telegram](https://t.me/fameboyq)

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
