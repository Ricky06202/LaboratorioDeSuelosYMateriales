#!/usr/bin/env python3
"""
Script para inicializar los permisos del sistema.
Este script debe ejecutarse una sola vez para crear los permisos necesarios.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/home/ricky/Documentos/C#/LaboratorioDeSuelosYMateriales/backend')

from app.db.session import SessionLocal
from app.models.user import Permission

def init_permissions():
    """Initialize system permissions."""
    db = SessionLocal()

    # Define permissions: (name, code)
    permissions_data = [
        ("Equipos", "equipment"),
        ("Directorio de Clientes", "customers"),
        ("Catálogo de Ensayos", "lab_services"),
        ("Agenda", "calendar"),
        ("Pedidos de Clientes", "customer_orders"),
        ("Cotizaciones", "quotations"),
        ("Órdenes de Servicio", "service_orders"),
    ]

    try:
        for name, code in permissions_data:
            # Check if permission already exists
            existing = db.query(Permission).filter(Permission.code == code).first()
            if not existing:
                permission = Permission(name=name, code=code)
                db.add(permission)
                print(f"Created permission: {name} ({code})")
            else:
                print(f"Permission already exists: {name} ({code})")

        db.commit()
        print("Permissions initialized successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error initializing permissions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_permissions()
