from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.api import deps
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Quotation])
def read_quotations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    customer_order_id: uuid.UUID = None,
) -> Any:
    """
    Retrieve quotations.
    """
    query = db.query(models.Quotation)
    if customer_order_id:
        query = query.filter(models.Quotation.customer_order_id == customer_order_id)
    quotations = query.offset(skip).limit(limit).all()
    return quotations

@router.post("/", response_model=schemas.Quotation)
def create_quotation(
    *,
    db: Session = Depends(deps.get_db),
    quotation_in: schemas.QuotationCreate,
) -> Any:
    """
    Create new quotation.
    """
    # Generar quotation_number autoincremental o UUID si no existe lógica
    # Para la lógica actual:
    import datetime
    year = datetime.datetime.now().year
    count = db.query(models.Quotation).filter(models.Quotation.year == year).count()
    quotation_number = f"LSMCH-{count+1:03d}-{year}"

    subtotal = sum([item.unit_price * item.amount for item in quotation_in.items])
    total = subtotal + quotation_in.mobilization_cost + quotation_in.viatics_cost

    db_quotation = models.Quotation(
        quotation_number=quotation_number,
        year=year,
        customer_id=quotation_in.customer_id,
        customer_order_id=quotation_in.customer_order_id,
        client_name=quotation_in.client_name,
        client_direction=quotation_in.client_direction,
        client_phone=quotation_in.client_phone,
        client_email=quotation_in.client_email,
        project_responsable=quotation_in.project_responsable,
        project_ruc=quotation_in.project_ruc,
        project_name=quotation_in.project_name,
        project_location=quotation_in.project_location,
        mobilization_cost=quotation_in.mobilization_cost,
        viatics_cost=quotation_in.viatics_cost,
        subtotal_amount=subtotal,
        total_amount=total,
        note=quotation_in.note,
        created_by="api" # ideally from user current
    )
    db.add(db_quotation)
    db.commit()
    db.refresh(db_quotation)

    # Add items
    for item_in in quotation_in.items:
        db_item = models.QuotationItem(
            quotation_id=db_quotation.id,
            item_norma=item_in.item_norma,
            item_sample=item_in.item_sample,
            amount=item_in.amount,
            description=item_in.description,
            unit_price=item_in.unit_price,
            total_price=item_in.unit_price * item_in.amount
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_quotation)
    return db_quotation

@router.get("/{id}", response_model=schemas.Quotation)
def read_quotation(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
) -> Any:
    """
    Get quotation by ID.
    """
    quotation = db.query(models.Quotation).filter(models.Quotation.id == id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

@router.delete("/{id}", response_model=schemas.Quotation)
def delete_quotation(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
) -> Any:
    """
    Delete a quotation.
    """
    quotation = db.query(models.Quotation).filter(models.Quotation.id == id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    db.delete(quotation)
    db.commit()
    return quotation

@router.get("/{id}/pdf")
def export_quotation_pdf(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
):
    """
    Generate PDF for quotation.
    """
    quotation = db.query(models.Quotation).filter(models.Quotation.id == id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
        
    from app.api.endpoints.pdf_utils import render_pdf
    from fastapi.responses import Response
    
    pdf_bytes = render_pdf("quotation.html", {"quotation": quotation})
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=Cotizacion_{quotation.quotation_number}.pdf"}
    )
