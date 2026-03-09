import psycopg2
import os

def upgrade():
    conn_str = "postgresql://lab_user:laboratorio77@localhost:5432/lab_suelos"
    print(f"Conectando a la base de datos...")
    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True
        cur = conn.cursor()
        
        columns = [
            ("tipo_fondo", "VARCHAR"),
            ("orden_compra", "VARCHAR"),
            ("solicitud_no", "VARCHAR"),
            ("tipo_bien", "VARCHAR"),
            ("fecha_recibido", "DATE"),
            ("id_asignado", "VARCHAR"),
            ("capacidad", "VARCHAR"),
            ("ubicacion_fisica", "VARCHAR")
        ]
        
        for col_name, col_type in columns:
            print(f"Añadiendo {col_name}...")
            try:
                cur.execute(f"ALTER TABLE equipos ADD COLUMN {col_name} {col_type};")
                print(f"OK: {col_name}")
            except Exception as e:
                print(f"ERROR/EXISTE: {col_name} -> {e}")
        
        cur.close()
        conn.close()
        print("Hecho.")
    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    upgrade()
