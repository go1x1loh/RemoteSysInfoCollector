from system_info import SystemInfoCollector
import json

def test_agent():
    print("Тестирование агента сбора системной информации...")
    
    # Создаем экземпляр коллектора без отправки данных на сервер
    collector = SystemInfoCollector("http://localhost:8000/api/v1/system-info")
    
    print("\n1. Базовая информация о системе:")
    print(f"Hostname: {collector.hostname}")
    print(f"IP Address: {collector.ip_address}")
    print(f"MAC Address: {collector.mac_address}")
    print(f"OS Info: {collector.os_info}")
    
    print("\n2. Информация о CPU:")
    cpu_usage = collector.get_cpu_usage()
    print(f"CPU Usage: {cpu_usage}%")
    
    print("\n3. Информация о памяти:")
    memory_info = collector.get_memory_info()
    print(f"Total Memory: {memory_info['total']:.2f} GB")
    print(f"Used Memory: {memory_info['used']:.2f} GB")
    
    print("\n4. Информация о дисках:")
    disk_info = collector.get_disk_usage()
    print(json.dumps(disk_info, indent=2))
    
    print("\n5. Топ процессов:")
    processes = collector.get_running_processes(limit=5)
    for proc in processes:
        print(f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, Memory: {proc.get('memory_percent', 0):.1f}%")
    
    print("\n6. Сетевая статистика:")
    network_stats = collector.get_network_stats()
    print(json.dumps(network_stats, indent=2))
    
    print("\nТестирование завершено!")

if __name__ == "__main__":
    test_agent()
