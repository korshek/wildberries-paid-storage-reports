# ⚡ Быстрый старт - Wildberries API Worker

## 🚀 За 5 минут к работающему приложению

### 1. Установите Docker Desktop
- **Mac**: https://www.docker.com/products/docker-desktop → Download for Mac
- **Windows**: https://www.docker.com/products/docker-desktop → Download for Windows
- **Linux**: `sudo apt install docker.io docker-compose`

### 2. Запустите Docker Desktop
- Дождитесь зеленого значка в строке меню

### 3. Откройте терминал и выполните:
```bash
# Перейдите в папку с проектом
cd путь/к/папке/WB_API_worker

# Запустите проект
docker-compose up -d

# Проверьте статус
docker-compose ps
```

### 4. Откройте браузер
```
http://localhost:5002
```

### 5. Готово! 🎉

---

## 🛑 Остановка проекта
```bash
docker-compose down
```

## 🔄 Перезапуск
```bash
docker-compose restart
```

## 📊 Просмотр логов
```bash
docker-compose logs -f
```

---

*Если что-то не работает - читайте подробный гайд `GUIDE_FOR_FRIEND.md`* 