from sqlalchemy import text
from app.db.session import engine

def upgrade_quotation():
    print("Iniciando actualización de la tabla quotations...")
    with engine.connect() as conn:
        print("Intentando añadir columna 'client_ruc'...")
        try:
            conn.execute(text("ALTER TABLE quotations ADD COLUMN client_ruc VARCHAR;"))
            print("Columna 'client_ruc' añadida con éxito.")
        except Exception as e:
            print(f"Columna 'client_ruc' ya existe o hubo un error: {e}")
        
        conn.commit()
    print("Actualización de quotations completada.")

if __name__ == "__main__":
    upgrade_quotation()
