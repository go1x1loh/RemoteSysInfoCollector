from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...db.base import get_db
from ...schemas.system_info import Computer, ComputerCreate, SystemInfo, SystemInfoCreate
from ...services.system_info import SystemInfoService

router = APIRouter()

@router.post("/computers/", response_model=Computer)
def create_computer(
    computer: ComputerCreate,
    db: Session = Depends(get_db)
):
    service = SystemInfoService(db)
    db_computer = service.get_computer_by_hostname(computer.hostname)
    if db_computer:
        raise HTTPException(status_code=400, detail="Computer already registered")
    return service.create_computer(computer)

@router.get("/computers/", response_model=List[Computer])
def read_computers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = SystemInfoService(db)
    computers = service.get_computers(skip=skip, limit=limit)
    return computers

@router.get("/computers/{computer_id}", response_model=Computer)
def read_computer(
    computer_id: int,
    db: Session = Depends(get_db)
):
    service = SystemInfoService(db)
    db_computer = service.get_computer(computer_id)
    if db_computer is None:
        raise HTTPException(status_code=404, detail="Computer not found")
    return db_computer

@router.post("/computers/{computer_id}/system-info/", response_model=SystemInfo)
def create_system_info(
    computer_id: int,
    system_info: SystemInfoCreate,
    db: Session = Depends(get_db)
):
    service = SystemInfoService(db)
    db_computer = service.get_computer(computer_id)
    if db_computer is None:
        raise HTTPException(status_code=404, detail="Computer not found")
    service.update_computer_last_seen(computer_id)
    return service.create_system_info(computer_id, system_info)

@router.get("/computers/{computer_id}/system-info/latest", response_model=SystemInfo)
def read_latest_system_info(
    computer_id: int,
    db: Session = Depends(get_db)
):
    service = SystemInfoService(db)
    if not service.get_computer(computer_id):
        raise HTTPException(status_code=404, detail="Computer not found")
    system_info = service.get_latest_system_info(computer_id)
    if system_info is None:
        raise HTTPException(status_code=404, detail="No system info found")
    return system_info

@router.get("/computers/{computer_id}/system-info/history", response_model=List[SystemInfo])
def read_system_info_history(
    computer_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = SystemInfoService(db)
    if not service.get_computer(computer_id):
        raise HTTPException(status_code=404, detail="Computer not found")
    return service.get_system_info_history(computer_id, skip=skip, limit=limit)
