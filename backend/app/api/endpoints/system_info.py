from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    logger.info(f"Registering computer: {computer.hostname}")
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
        logger.error(f"Computer with ID {computer_id} not found")
        raise HTTPException(status_code=404, detail="Computer not found")
    
    logger.info(f"Received system info for computer {computer_id}")
    logger.info(f"System info data: {system_info.dict()}")
    
    try:
        service.update_computer_last_seen(computer_id)
        db_system_info = service.create_system_info(computer_id, system_info)
        return db_system_info
    except Exception as e:
        logger.error(f"Error creating system info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

@router.get("/computers/{computer_id}/details", response_model=Computer)
def get_computer_details(
    computer_id: int,
    db: Session = Depends(get_db)
):
    service = SystemInfoService(db)
    
    logger.info(f"Retrieving details for computer {computer_id}")
    
    computer = service.get_computer_with_system_info(computer_id)
    if computer is None:
        logger.error(f"Computer with ID {computer_id} not found")
        raise HTTPException(status_code=404, detail="Computer not found")
    
    return computer
