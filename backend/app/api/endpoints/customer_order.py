from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import datetime

from app.api import deps
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.CustomerOrder])
def read_customer_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve customer orders.
    """
    orders = db.query(models.CustomerOrder).offset(skip).limit(limit).all()
    return orders

@router.post("/", response_model=schemas.CustomerOrder)
def create_customer_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.CustomerOrderCreate,
) -> Any:
    """
    Create new customer order.
    """
    # Logic for order number RA-LSMCH-037-XXX-YYYY
    year = datetime.datetime.now().year
    count = db.query(models.CustomerOrder).filter(
        models.CustomerOrder.order_number.like(f"RA-LSMCH-037-%-{year}")
    ).count()
    order_number = f"RA-LSMCH-037-{count+1:03d}-{year}"

    db_order = models.CustomerOrder(
        order_number=order_number,
        date=order_in.date,
        client_name=order_in.client_name,
        client_direction=order_in.client_direction,
        client_ruc=order_in.client_ruc,
        client_dv=order_in.client_dv,
        client_phone=order_in.client_phone,
        project_name=order_in.project_name,
        project_location=order_in.project_location,
        project_responsable=order_in.project_responsable,
        project_responsable_phone=order_in.project_responsable_phone,
        project_responsable_email=order_in.project_responsable_email,
        observations=order_in.observations,
        attended_by=order_in.attended_by,
        approved_quotation_number=order_in.approved_quotation_number,
        created_by="api"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add items
    for item_in in order_in.items:
        db_item = models.CustomerOrderItem(
            customer_order_id=db_order.id,
            item_number=item_in.item_number,
            test_name=item_in.test_name,
            sample_type=item_in.sample_type,
            test_count=item_in.test_count,
            norm_method=item_in.norm_method
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/{id}", response_model=schemas.CustomerOrder)
def read_customer_order(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
) -> Any:
    """
    Get customer order by ID.
    """
    order = db.query(models.CustomerOrder).filter(models.CustomerOrder.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Customer Order not found")
    return order

@router.delete("/{id}", response_model=schemas.CustomerOrder)
def delete_customer_order(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
) -> Any:
    """
    Delete a customer order.
    """
    order = db.query(models.CustomerOrder).filter(models.CustomerOrder.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Customer Order not found")
    db.delete(order)
    db.commit()
    return order

@router.get("/{id}/pdf")
def export_customer_order_pdf(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
):
    """
    Generate PDF for customer order.
    """
    order = db.query(models.CustomerOrder).filter(models.CustomerOrder.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Customer Order not found")
        
    from app.api.endpoints.pdf_utils import render_pdf
    from fastapi.responses import Response
    
    pdf_bytes = render_pdf("customer_order.html", {"order": order})
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=Pedido_{order.order_number}.pdf"}
    )
