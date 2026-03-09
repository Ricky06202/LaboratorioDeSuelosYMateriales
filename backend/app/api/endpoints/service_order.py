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

@router.get("/{id}/sample_receipt")
def export_sample_receipt_pdf(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
):
    """
    Generate PDF for sample receipt related to a service order.
    """
    service_order = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == id).first()
    if not service_order:
        raise HTTPException(status_code=404, detail="Service Order not found")
        
    # Mock data linked to the order for demonstration
    data = {
        "receipt_number": f"RM-{service_order.order_number}",
        "client_name": getattr(service_order, 'client_name', 'N/A'),
        "service_order_number": service_order.order_number,
        "brought_by": "Cliente",
        "sample_types": ["Cilindro de concreto de 150 x 300 mm"],
        "conditions": [{"client_id": "M-01", "quantity": "3", "condition": "Buen estado"}],
        "storage_area": "Área de muestras para ensayar",
        "observations": getattr(service_order, 'observations', ''),
        "delivered_by": getattr(service_order, 'applicant_name', ''),
        "received_by": getattr(service_order, 'attended_by', ''),
        "delivered_date": str(service_order.date.date()) if hasattr(service_order, 'date') and service_order.date else "",
        "received_date": str(service_order.date.date()) if hasattr(service_order, 'date') and service_order.date else ""
    }
    
    from app.api.endpoints.pdf_utils import render_pdf
    from fastapi.responses import Response
    
    pdf_bytes = render_pdf("sample_receipt.html", {"data": data})
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=ReciboMuestra_{service_order.order_number}.pdf"}
    )

@router.get("/reports/sample_control", response_class=Response)
def export_sample_control_pdf(
    *,
    db: Session = Depends(deps.get_db),
):
    """
    Generate PDF for sample control registry (RT-LSMCH-026).
    """
    # For now, it pulls recent service orders to mock data
    service_orders = db.query(models.ServiceOrder).order_by(models.ServiceOrder.date.desc()).limit(10).all()
    
    items = []
    
    for order in service_orders:
        items.append({
            "receipt_no": f"RM-{order.order_number}",
            "work_request_no": order.order_number,
            "lab_id": f"LAB-{order.id.hex[:6].upper()}",
            "entry_date": str(order.date.date()) if hasattr(order, 'date') and order.date else "",
            "to_test_by": order.attended_by,
            "to_test_date": str(order.date.date()) if hasattr(order, 'date') and order.date else "",
            "tested_by": "",
            "tested_date": "",
            "discard_zone_by": "",
            "discard_zone_date": "",
            "client_retrieved_by": "",
            "client_retrieved_date": "",
            "discard_by": "",
            "discard_date": ""
        })
        
    from app.api.endpoints.pdf_utils import render_pdf
    from fastapi.responses import Response
    
    pdf_bytes = render_pdf("sample_control_registry.html", {"items": items})
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": "attachment; filename=ControlMuestras.pdf"}
    )
