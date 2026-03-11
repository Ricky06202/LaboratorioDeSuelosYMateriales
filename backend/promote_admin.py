import sys
import os
from sqlalchemy.orm import Session

# Add the current directory to path to import app
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.user import User, Role

def promote_user(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"Error: Usuario con email {email} no encontrado.")
            return
        
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if not admin_role:
            print("Error: El rol 'Admin' no existe. Asegúrate de que la API haya corrido al menos una vez.")
            return
        
        user.role_id = admin_role.id
        db.commit()
        print(f"Éxito: El usuario {email} ahora es Administrador.")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python promote_admin.py <email>")
    else:
        promote_user(sys.argv[1])
