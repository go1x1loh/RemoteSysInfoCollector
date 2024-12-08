# System Information Collector

Проект для автоматизированного сбора системной информации с удаленных компьютеров.

## 📂 Project Structure

```
system-information-collector/
│
├── backend/                   # Backend FastAPI application
│   ├── app/
│   │   ├── api/               # API endpoint definitions
│   │   │   └── endpoints/
│   │   ├── core/              # Core configuration and settings
│   │   ├── db/                # Database configuration and initialization
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic validation schemas
│   │   └── services/          # Business logic and service layers
│   │
│   ├── tests/                 # Backend unit and integration tests
│   ├── alembic/               # Database migration scripts
│   ├── requirements.txt       # Python dependencies
│   └── main.py                # FastAPI application entry point
│
├── agent/                     # System information collection agent
│   ├── system_info.py         # Main agent script for data collection
│   ├── config.py              # Agent configuration
│   └── utils/                 # Utility functions
│
├── frontend/                  # React.js frontend application
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── components/        # React UI components
│   │   ├── services/          # API service calls
│   │   ├── utils/             # Frontend utility functions
│   │   ├── App.js             # Main React application
│   │   └── index.js           # Entry point
│   ├── package.json           # Frontend dependencies
│   └── README.md              # Frontend-specific documentation
│
├── docs/                      # Project documentation
│
├── .env                       # Environment configuration
├── .gitignore
├── README.md                  # Project overview and documentation
└── docker-compose.yml         # Docker containerization configuration
```

### 🔍 Key Directories Explained

- **`backend/`**: Contains the core backend logic
  - Handles system information processing
  - Manages database interactions
  - Provides RESTful API endpoints

- **`agent/`**: Responsible for system metrics collection
  - Gathers system information
  - Sends data to backend
  - Configurable data collection

- **`frontend/`**: React-based user interface
  - Displays system information
  - Provides interactive dashboards
  - Manages API interactions

- **`docs/`**: Additional project documentation
  - Technical specifications
  - API references
  - Development guides

### 🛠 Configuration Files

- `.env`: Stores environment-specific configurations
- `docker-compose.yml`: Defines multi-container Docker setup
- Backend `requirements.txt`: Python package dependencies
- Frontend `package.json`: JavaScript/React dependencies

### 📊 Data Flow

1. Agent collects system metrics
2. Agent sends data to Backend API
3. Backend stores data in PostgreSQL
4. Frontend retrieves and displays data

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
