from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.api import deps
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.ServiceOrder])
def read_service_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve service orders.
    """
    service_orders = db.query(models.ServiceOrder).offset(skip).limit(limit).all()
    return service_orders

@router.post("/", response_model=schemas.ServiceOrder)
def create_service_order(
    *,
    db: Session = Depends(deps.get_db),
    service_order_in: schemas.ServiceOrderCreate,
) -> Any:
    """
    Create new service order.
    """
    import datetime
    year = datetime.datetime.now().year
    count = db.query(models.ServiceOrder).filter(models.ServiceOrder.year == year).count()
    order_number = f"LSMCH-{count+1:03d}-{year}"

    db_obj_data = service_order_in.model_dump()
    db_obj = models.ServiceOrder(**db_obj_data, order_number=order_number, year=year, created_by="api")
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/{id}", response_model=schemas.ServiceOrder)
def read_service_order(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
) -> Any:
    """
    Get service order by ID.
    """
    service_order = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == id).first()
    if not service_order:
        raise HTTPException(status_code=404, detail="Service Order not found")
    return service_order

@router.delete("/{id}", response_model=schemas.ServiceOrder)
def delete_service_order(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
) -> Any:
    """
    Delete a service order.
    """
    service_order = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == id).first()
    if not service_order:
        raise HTTPException(status_code=404, detail="Service Order not found")
    db.delete(service_order)
    db.commit()
    return service_order

@router.get("/{id}/pdf")
def export_service_order_pdf(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
):
    """
    Generate PDF for service order.
    """
    service_order = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == id).first()
    if not service_order:
        raise HTTPException(status_code=404, detail="Service Order not found")
        
    from app.api.endpoints.pdf_utils import render_pdf
    from fastapi.responses import Response
    
    pdf_bytes = render_pdf("service_order.html", {"order": service_order})
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=OrdenServicio_{service_order.order_number}.pdf"}
    )
