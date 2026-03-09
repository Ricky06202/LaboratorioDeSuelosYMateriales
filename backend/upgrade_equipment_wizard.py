from sqlalchemy import text
from app.db.session import engine

def upgrade_equipment_wizard():
    print("Iniciando actualización de columnas para el Wizard de Equipos...")
    columns_to_add = [
        ("tipo_fondo", "VARCHAR"),
        ("orden_compra", "VARCHAR"),
        ("solicitud_no", "VARCHAR"),
        ("tipo_bien", "VARCHAR"),
        ("fecha_recibido", "DATE"),
        ("id_asignado", "VARCHAR"),
        ("capacidad", "VARCHAR"),
        ("ubicacion_fisica", "VARCHAR")
    ]
    
    with engine.connect() as conn:
        for col_name, col_type in columns_to_add:
            print(f"Intentando añadir columna '{col_name}'...")
            try:
                # Basic check to avoid error log noise if possible, though try/except is safer in Postgres
                conn.execute(text(f"ALTER TABLE equipos ADD COLUMN {col_name} {col_type};"))
                print(f"Columna '{col_name}' añadida con éxito.")
            except Exception as e:
                # If column already exists, we catch the exception
                print(f"Columna '{col_name}' no pudo ser añadida (posiblemente ya existe): {e}")
        
        conn.commit()
    print("Actualización de esquema completada.")

if __name__ == "__main__":
    upgrade_equipment_wizard()
