#!/usr/bin/env python3
"""
Script para actualizar los nombres de los permisos del sistema.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/home/ricky/Documentos/C#/LaboratorioDeSuelosYMateriales/backend')

from app.db.session import SessionLocal
from app.models.user import Permission

def update_permission_names():
    """Update permission names to match navbar text."""
    db = SessionLocal()

    # Define new names for permissions: (code, new_name)
    permission_updates = {
        "users": "Gestión de Usuarios",
        "roles": "Gestión de Roles",
        "equipment": "Equipos",
        "quotations": "Cotizaciones",
        "service_orders": "Órdenes de Servicio",
        "customer_orders": "Pedidos de Clientes",
        "customers": "Directorio de Clientes",
        "calendar": "Agenda de Actividades",
        "lab_services": "Catálogo de Ensayos",
    }

    try:
        for code, new_name in permission_updates.items():
            permission = db.query(Permission).filter(Permission.code == code).first()
            if permission:
                old_name = permission.name
                permission.name = new_name
                db.add(permission)
                print(f"Updated permission {code}: '{old_name}' -> '{new_name}'")
            else:
                print(f"Permission not found: {code}")

        db.commit()
        print("\nPermission names updated successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error updating permissions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_permission_names()
