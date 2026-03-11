from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.api import deps
from app.services.calendar_service import calendar_service
from app.schemas.calendar import CalendarActivitySchema, CalendarActivityCreate, CalendarActivityUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CalendarActivitySchema])
def read_activities(
    db: Session = Depends(deps.get_db),
    start: datetime = None,
    end: datetime = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return calendar_service.get_activities(db, start=start, end=end)

@router.post("/", response_model=CalendarActivitySchema)
def create_activity(
    *,
    db: Session = Depends(deps.get_db),
    activity_in: CalendarActivityCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return calendar_service.create_activity(db, activity=activity_in)

@router.put("/{activity_id}", response_model=CalendarActivitySchema)
def update_activity(
    *,
    db: Session = Depends(deps.get_db),
    activity_id: str,
    activity_in: CalendarActivityUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return calendar_service.update_activity(db, activity_id=activity_id, activity=activity_in)

@router.delete("/{activity_id}", response_model=CalendarActivitySchema)
def delete_activity(
    *,
    db: Session = Depends(deps.get_db),
    activity_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return calendar_service.delete_activity(db, activity_id=activity_id)
