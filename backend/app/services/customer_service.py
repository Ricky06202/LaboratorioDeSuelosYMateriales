from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Tuple
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CustomerService:
    @staticmethod
    def get_customers(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> Tuple[List[Customer], int]:
        query = db.query(Customer)
        if search:
            query = query.filter(
                or_(
                    Customer.name.ilike(f"%{search}%"),
                    Customer.ruc.ilike(f"%{search}%")
                )
            )
        total = query.count()
        return query.offset(skip).limit(limit).all(), total

    @staticmethod
    def get_customer(db: Session, customer_id: str):
        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate):
        db_obj = Customer(**customer.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_customer(db: Session, customer_id: str, customer: CustomerUpdate):
        db_obj = db.query(Customer).filter(Customer.id == customer_id).first()
        if not db_obj:
            return None
        
        obj_data = customer.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete_customer(db: Session, customer_id: str):
        db_obj = db.query(Customer).filter(Customer.id == customer_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

customer_service = CustomerService()
