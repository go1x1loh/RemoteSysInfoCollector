from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

from ..models.system_info import Computer, SystemInfo
from ..schemas.system_info import ComputerCreate, SystemInfoCreate

class SystemInfoService:
    def __init__(self, db: Session):
        self.db = db

    def get_computer(self, computer_id: int) -> Optional[Computer]:
        return self.db.query(Computer).filter(Computer.id == computer_id).first()

    def get_computer_by_hostname(self, hostname: str) -> Optional[Computer]:
        return self.db.query(Computer).filter(Computer.hostname == hostname).first()

    def get_computers(self, skip: int = 0, limit: int = 100) -> List[Computer]:
        return self.db.query(Computer).offset(skip).limit(limit).all()

    def create_computer(self, computer: ComputerCreate) -> Computer:
        # Ищем существующий компьютер по hostname
        logger.info(f"Attempting to create/update computer: {computer}")
        
        try:
            # Validate input data
            if not computer.hostname:
                raise ValueError("Hostname cannot be empty")
            
            # Check for existing computer
            existing_computer = self.get_computer_by_hostname(computer.hostname)
            
            # Если компьютер уже существует, обновляем его данные
            if existing_computer:
                logger.info(f"Computer {computer.hostname} already exists. Updating.")
                existing_computer.ip_address = computer.ip_address
                existing_computer.mac_address = computer.mac_address
                existing_computer.os_info = computer.os_info
                existing_computer.last_seen = datetime.utcnow()
                
                try:
                    self.db.commit()
                    self.db.refresh(existing_computer)
                except Exception as commit_error:
                    logger.error(f"Error committing existing computer update: {commit_error}")
                    self.db.rollback()
                    raise
                
                return existing_computer
            
            # Если компьютер новый, создаем его
            logger.info(f"Creating new computer: {computer.hostname}")
            
            # Convert ComputerCreate to dict, ensuring all fields are present
            computer_dict = {
                'hostname': computer.hostname,
                'ip_address': computer.ip_address,
                'mac_address': computer.mac_address,
                'os_info': computer.os_info,
                'last_seen': datetime.utcnow()
            }
            
            db_computer = Computer(**computer_dict)
            
            try:
                self.db.add(db_computer)
                self.db.commit()
                self.db.refresh(db_computer)
            except Exception as create_error:
                logger.error(f"Error creating new computer: {create_error}")
                self.db.rollback()
                raise
            
            return db_computer
        
        except Exception as e:
            logger.error(f"Unexpected error in create_computer: {e}")
            self.db.rollback()
            raise

    def update_computer_last_seen(self, computer_id: int) -> Computer:
        db_computer = self.get_computer(computer_id)
        if db_computer:
            db_computer.last_seen = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_computer)
        return db_computer

    def create_system_info(self, computer_id: int, system_info: SystemInfoCreate) -> SystemInfo:
        db_system_info = SystemInfo(
            computer_id=computer_id,
            cpu_usage=system_info.cpu_usage,
            memory_total=system_info.memory_total,
            memory_used=system_info.memory_used,
            disk_usage=system_info.disk_usage,
            running_processes=system_info.running_processes,
            network_stats=system_info.network_stats
        )
        self.db.add(db_system_info)
        self.db.commit()
        self.db.refresh(db_system_info)
        return db_system_info

    def get_latest_system_info(self, computer_id: int) -> Optional[SystemInfo]:
        return (self.db.query(SystemInfo)
                .filter(SystemInfo.computer_id == computer_id)
                .order_by(SystemInfo.timestamp.desc())
                .first())

    def get_system_info_history(
        self, computer_id: int, skip: int = 0, limit: int = 100
    ) -> List[SystemInfo]:
        return (self.db.query(SystemInfo)
                .filter(SystemInfo.computer_id == computer_id)
                .order_by(SystemInfo.timestamp.desc())
                .offset(skip)
                .limit(limit)
                .all())

    def get_computer_with_system_info(self, computer_id: int) -> Optional[Computer]:
        """
        Retrieve a computer with its latest system information.
        
        :param computer_id: ID of the computer
        :return: Computer object with latest system info, or None
        """
        computer = self.get_computer(computer_id)
        if computer:
            # Get the latest system info for this computer
            latest_system_info = (
                self.db.query(SystemInfo)
                .filter(SystemInfo.computer_id == computer_id)
                .order_by(SystemInfo.timestamp.desc())
                .first()
            )
            
            # If system info exists, add it to the computer's system_info list
            if latest_system_info:
                computer.system_info = [latest_system_info]
        
        return computer
