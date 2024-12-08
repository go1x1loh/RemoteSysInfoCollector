# System Information Collector

Проект для автоматизированного сбора системной информации с удаленных компьютеров.

## Структура проекта

```
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Конфигурация
│   │   ├── db/          # База данных
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Бизнес-логика
│   └── main.py          # Точка входа
├── frontend/            # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   └── package.json
└── agent/              # Агент для сбора информации
    └── system_info.py
```

## Установка и запуск

### Backend

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл .env с настройками:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
```

4. Запустите сервер:
```bash
uvicorn backend.main:app --reload
```

### Frontend

1. Установите зависимости:
```bash
cd frontend
npm install
```

2. Запустите development сервер:
```bash
npm start
```

### Agent

1. Скопируйте агент на целевой компьютер
2. Установите необходимые зависимости
3. Настройте конфигурацию подключения к серверу
4. Запустите агент
