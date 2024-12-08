from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional

class SystemInfoBase(BaseModel):
    cpu_usage: float
    memory_total: float
    memory_used: float
    disk_usage: Dict
    running_processes: List[Dict]
    network_stats: Dict

class SystemInfoCreate(SystemInfoBase):
    pass

class SystemInfo(SystemInfoBase):
    id: int
    computer_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ComputerBase(BaseModel):
    hostname: str
    ip_address: str
    mac_address: str
    os_info: str

class ComputerCreate(ComputerBase):
    pass

class Computer(ComputerBase):
    id: int
    created_at: datetime
    last_seen: datetime
    system_info: Optional[List[SystemInfo]] = []

    class Config:
        from_attributes = True
