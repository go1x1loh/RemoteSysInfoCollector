import psutil
import platform
import requests
import time
import socket
import uuid
from datetime import datetime
from typing import Dict, List
import os
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SystemInfoCollector:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.hostname)
        self.mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                   for elements in range(0,2*6,2)][::-1])
        self.os_info = f"{platform.system()} {platform.release()}"

    def register_computer(self):
        computer_data = {
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "os_info": self.os_info
        }
        try:
            response = requests.post(f"{self.api_url}/system-info/computers/", 
                                     json=computer_data, 
                                     timeout=10)  # Добавляем таймаут
            response.raise_for_status()
            logging.info(f"Successfully registered computer: {computer_data}")
            logging.info(f"Response from server: {response.json()}")
            return response.json().get('id')
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to register computer: {e}")
            logging.error(f"URL: {self.api_url}/system-info/computers/")
            logging.error(f"Request data: {computer_data}")
            raise

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

    def send_system_info(self, computer_id: int, system_info: Dict):
        logging.info(f"Sending system info for computer {computer_id}")
        logging.info(f"System info data: {system_info}")
        
        try:
            response = requests.post(
                f"{self.api_url}/system-info/computers/{computer_id}/system-info/", 
                json=system_info, 
                timeout=10
            )
            response.raise_for_status()
            logging.info("System info sent successfully")
            logging.info(f"Server response: {response.json()}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send system info: {e}")
            logging.error(f"URL: {self.api_url}/system-info/computers/{computer_id}/system-info/")
            logging.error(f"Data: {system_info}")
            raise

    def collect_and_send_info(self, computer_id: int):
        try:
            memory_info = self.get_memory_info()
            data = {
                "computer_id": computer_id,
                "cpu_usage": self.get_cpu_usage(),
                "memory_total": memory_info['total'],
                "memory_used": memory_info['used'],
                "disk_usage": self.get_disk_usage(),
                "running_processes": self.get_running_processes(),
                "network_stats": self.get_network_stats(),
                "timestamp": datetime.now().isoformat()
            }
            self.send_system_info(computer_id, data)
        except Exception as e:
            logging.error(f"Failed to collect and send system info: {e}")
            raise

def main():
    API_URL = os.getenv('SYSTEM_INFO_API_URL', 'http://localhost:8000/api/v1')
    INTERVAL = int(os.getenv('SYSTEM_INFO_INTERVAL', 60))
    MAX_RETRIES = int(os.getenv('SYSTEM_INFO_MAX_RETRIES', 5))

    collector = SystemInfoCollector(API_URL)
    
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            computer_id = collector.register_computer()
            
            while True:
                try:
                    collector.collect_and_send_info(computer_id)
                    time.sleep(INTERVAL)
                except requests.exceptions.RequestException:
                    logging.warning(f"Failed to send system info. Retrying in {INTERVAL} seconds...")
                    time.sleep(INTERVAL)
        
        except requests.exceptions.RequestException as e:
            retry_count += 1
            logging.warning(f"Registration failed (attempt {retry_count}/{MAX_RETRIES}): {e}")
            time.sleep(INTERVAL)
    
    logging.error("Failed to register computer after maximum retries")

if __name__ == "__main__":
    main()
