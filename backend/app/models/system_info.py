from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# Import Base from a function to avoid circular import
from ..db.base import Base as DeclarativeBase

class Computer(DeclarativeBase):
    __tablename__ = "computers"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, unique=True, index=True)
    ip_address = Column(String)
    mac_address = Column(String)
    os_info = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    system_info = relationship("SystemInfo", back_populates="computer")

class SystemInfo(DeclarativeBase):
    __tablename__ = "system_info"

    id = Column(Integer, primary_key=True, index=True)
    computer_id = Column(Integer, ForeignKey("computers.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    cpu_usage = Column(Float)
    memory_total = Column(Float)
    memory_used = Column(Float)
    disk_usage = Column(JSON)
    running_processes = Column(JSON)
    network_stats = Column(JSON)

    computer = relationship("Computer", back_populates="system_info")
