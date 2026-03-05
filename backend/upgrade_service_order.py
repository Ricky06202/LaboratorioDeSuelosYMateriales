from sqlalchemy import text
from app.db.session import engine

def upgrade_service_order():
    print("Iniciando actualización de la tabla service_orders...")
    with engine.connect() as conn:
        columns_to_add = [
            ("client_dv", "VARCHAR"),
            ("quotation_ref", "VARCHAR"),
            ("applicant_id_number", "VARCHAR")
        ]
        
        for col_name, col_type in columns_to_add:
            print(f"Intentando añadir columna '{col_name}'...")
            try:
                # Check if column exists first (optional but safer)
                conn.execute(text(f"ALTER TABLE service_orders ADD COLUMN {col_name} {col_type};"))
                print(f"Columna '{col_name}' añadida con éxito.")
            except Exception as e:
                print(f"Columna '{col_name}' ya existe o hubo un error: {e}")
        
        conn.commit()
    print("Actualización de service_orders completada.")

if __name__ == "__main__":
    upgrade_service_order()
