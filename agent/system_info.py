import psutil
import platform
import requests
import time
import socket
import uuid
from datetime import datetime
from typing import Dict

class SystemInfoCollector:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.hostname)
        self.mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                   for elements in range(0,2*6,2)][::-1])
        self.os_info = f"{platform.system()} {platform.release()}"

    def register_computer(self) -> int:
        """Register computer with the server and return computer_id"""
        data = {
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "os_info": self.os_info
        }
        response = requests.post(f"{self.api_url}/computers/", json=data)
        response.raise_for_status()
        return response.json()["id"]

    def get_cpu_usage(self) -> float:
        return psutil.cpu_percent(interval=1)

    def get_memory_info(self) -> Dict[str, float]:
        memory = psutil.virtual_memory()
        return {
            "total": memory.total / (1024 ** 3),  # GB
            "used": memory.used / (1024 ** 3)     # GB
        }

    def get_disk_usage(self) -> Dict[str, Dict]:
        disk_info = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.mountpoint] = {
                    "total": usage.total / (1024 ** 3),  # GB
                    "used": usage.used / (1024 ** 3),    # GB
                    "percent": usage.percent
                }
            except Exception:
                continue
        return disk_info

    def get_running_processes(self, limit: int = 10) -> list:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:limit]

    def get_network_stats(self) -> Dict:
        network_stats = psutil.net_io_counters()
        return {
            "bytes_sent": network_stats.bytes_sent,
            "bytes_recv": network_stats.bytes_recv,
            "packets_sent": network_stats.packets_sent,
            "packets_recv": network_stats.packets_recv
        }

    def collect_and_send_info(self, computer_id: int):
        """Collect system information and send it to the server"""
        memory_info = self.get_memory_info()
        system_info = {
            "cpu_usage": self.get_cpu_usage(),
            "memory_total": memory_info["total"],
            "memory_used": memory_info["used"],
            "disk_usage": self.get_disk_usage(),
            "running_processes": self.get_running_processes(),
            "network_stats": self.get_network_stats()
        }

        response = requests.post(
            f"{self.api_url}/computers/{computer_id}/system-info/",
            json=system_info
        )
        response.raise_for_status()
        return response.json()

def main():
    API_URL = "http://localhost:8000/api/v1/system-info"  # Измените на реальный URL сервера
    INTERVAL = 60  # Интервал сбора данных в секундах

    collector = SystemInfoCollector(API_URL)
    
    try:
        computer_id = collector.register_computer()
        print(f"Successfully registered computer with ID: {computer_id}")
        
        while True:
            try:
                collector.collect_and_send_info(computer_id)
                print(f"Successfully sent system info at {datetime.now()}")
            except Exception as e:
                print(f"Error sending system info: {e}")
            
            time.sleep(INTERVAL)
    except Exception as e:
        print(f"Error registering computer: {e}")

if __name__ == "__main__":
    main()
