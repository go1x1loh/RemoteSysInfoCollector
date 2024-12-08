from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional

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
        db_computer = Computer(**computer.dict())
        self.db.add(db_computer)
        self.db.commit()
        self.db.refresh(db_computer)
        return db_computer

    def update_computer_last_seen(self, computer_id: int) -> Computer:
        db_computer = self.get_computer(computer_id)
        if db_computer:
            db_computer.last_seen = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_computer)
        return db_computer

    def create_system_info(self, computer_id: int, system_info: SystemInfoCreate) -> SystemInfo:
        db_system_info = SystemInfo(**system_info.dict(), computer_id=computer_id)
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
