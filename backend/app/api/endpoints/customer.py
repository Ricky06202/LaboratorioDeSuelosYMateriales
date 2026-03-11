from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.services.customer_service import customer_service
from app.schemas.customer import CustomerSchema, CustomerCreate, CustomerUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CustomerSchema])
def read_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    customers, _ = customer_service.get_customers(db, skip=skip, limit=limit, search=search)
    return customers

@router.post("/", response_model=CustomerSchema)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_in: CustomerCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return customer_service.create_customer(db, customer=customer_in)

@router.get("/{customer_id}", response_model=CustomerSchema)
def read_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    customer = customer_service.get_customer(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=CustomerSchema)
def update_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: str,
    customer_in: CustomerUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    customer = customer_service.get_customer(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_service.update_customer(db, customer_id=customer_id, customer=customer_in)

@router.delete("/{customer_id}", response_model=CustomerSchema)
def delete_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    customer = customer_service.get_customer(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_service.delete_customer(db, customer_id=customer_id)
