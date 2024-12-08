#!/bin/bash

# Проверка наличия PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL не установлен. Установка..."
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен. Установка..."
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# Проверка наличия Node.js
if ! command -v node &> /dev/null; then
    echo "Node.js не установлен. Установка..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Создание виртуального окружения Python и установка зависимостей
echo "Настройка backend..."
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r requirements.txt

# Инициализация базы данных
echo "Инициализация базы данных..."
python backend/app/db/init_db.py

# Установка зависимостей frontend
echo "Настройка frontend..."
cd frontend
npm install
cd ..

# Создание скрипта для запуска
echo "Создание скрипта запуска..."
cat > start.sh << 'EOL'
#!/bin/bash

# Запуск backend
echo "Запуск backend..."
source backend/venv/bin/activate
uvicorn backend.app.main:app --reload &

# Запуск frontend
echo "Запуск frontend..."
cd frontend
npm start &

# Запуск агента
echo "Запуск агента..."
source backend/venv/bin/activate
python agent/system_info.py &

echo "Все сервисы запущены!"
EOL

chmod +x start.sh

echo "Установка завершена! Для запуска проекта выполните: ./start.sh"
