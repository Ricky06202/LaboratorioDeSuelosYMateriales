from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, equipment, quotation, service_order, customer_order
from app.db.session import engine
from app.db.base import Base
from fastapi.responses import JSONResponse
import traceback
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") == "True":
        yield
        return
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    
    # Check for missing columns in equipments table for the Wizard
    from sqlalchemy import text
    columns_to_add = [
        ("tipo_fondo", "VARCHAR"),
        ("orden_compra", "VARCHAR"),
        ("solicitud_no", "VARCHAR"),
        ("tipo_bien", "VARCHAR"),
        ("fecha_recibido", "DATE"),
        ("id_asignado", "VARCHAR"),
        ("capacidad", "VARCHAR"),
        ("ubicacion_fisica", "VARCHAR"),
        ("proveedor", "VARCHAR"),
        ("estado_aprobacion", "VARCHAR"),
        ("observaciones", "TEXT"),
        ("verificado_por", "VARCHAR"),
        ("revisado_por", "VARCHAR"),
        ("fecha_verificacion", "DATE"),
        ("fecha_revision", "DATE"),
        ("rango_calibracion", "VARCHAR"),
        ("frecuencia_calibracion", "INTEGER"),
        ("metodo_mantenimiento", "VARCHAR")
    ]
    # Add criteria columns 1-14
    for i in range(1, 15):
        columns_to_add.append((f"criteria_{i}", "BOOLEAN DEFAULT TRUE"))

    with engine.connect() as conn:
        # Check equipos table
        for col_name, col_type in columns_to_add:
            try:
                conn.execute(text(f"ALTER TABLE equipos ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
            except Exception as e:
                print(f"Error checking column {col_name} in equipos: {e}")
        
        # Check calibraciones table columns (just in case)
        calib_cols = [("empresa_certificadora", "VARCHAR"), ("certificado_url", "VARCHAR")]
        for col_name, col_type in calib_cols:
            try:
                conn.execute(text(f"ALTER TABLE calibraciones ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
            except Exception:
                pass
        conn.commit()
    yield

app = FastAPI(title="Laboratorio de Suelos API", lifespan=lifespan)

@app.exception_handler(Exception)
async def debug_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "trace": traceback.format_exc()},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(equipment.router, prefix="/api/equipos", tags=["equipos"])
app.include_router(quotation.router, prefix="/api/cotizaciones", tags=["cotizaciones"])
app.include_router(service_order.router, prefix="/api/ordenes-servicio", tags=["ordenes_servicio"])
app.include_router(customer_order.router, prefix="/api/pedidos", tags=["pedidos"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Laboratorio de Suelos"}
