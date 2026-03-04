from sqlalchemy import text
from app.db.session import engine

def upgrade_db():
    print("Iniciando actualización de la base de datos...")
    with engine.connect() as conn:
        print("Habilitando PostGIS...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        
        print("Añadiendo columnas a equipos...")
        try:
            conn.execute(text("ALTER TABLE equipos ADD COLUMN ubicacion geometry(POINT,4326);"))
            print("Columna 'ubicacion' añadida.")
        except Exception as e:
            print(f"Columna 'ubicacion' ya existe o error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE equipos ADD COLUMN fecha_proxima_calibracion DATE;"))
            print("Columna 'fecha_proxima_calibracion' añadida.")
        except Exception as e:
            print(f"Columna 'fecha_proxima_calibracion' ya existe o error: {e}")

        # Note: Removing FOREIGN KEY ON DELETE CASCADE constraint requires identifying it first.
        # But wait, we can just do it. Let's find the constraint name.
        print("Removiendo restricciones CASCADE de calibraciones_equipo_id_fkey...")
        try:
            conn.execute(text("ALTER TABLE calibraciones DROP CONSTRAINT calibraciones_equipo_id_fkey;"))
            conn.execute(text("ALTER TABLE calibraciones ADD CONSTRAINT calibraciones_equipo_id_fkey FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE RESTRICT;"))
            print("Restricción cambiada a ON DELETE RESTRICT.")
        except Exception as e:
            print(f"Error modificando constraint (podría ya estar aplicada): {e}")

        conn.commit()
    print("Actualización completada.")

if __name__ == "__main__":
    upgrade_db()
