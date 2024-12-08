import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_database():
    # Параметры подключения к PostgreSQL
    params = {
        'host': os.getenv('POSTGRES_SERVER', 'localhost'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'database': 'postgres'  # Подключаемся к дефолтной базе для создания нашей
    }

    try:
        # Подключаемся к PostgreSQL
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Проверяем существование базы данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'system_info'")
        exists = cursor.fetchone()
        
        if not exists:
            # Создаем базу данных
            cursor.execute('CREATE DATABASE system_info')
            print("База данных system_info успешно создана")
        else:
            print("База данных system_info уже существует")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        return False

if __name__ == "__main__":
    init_database()
