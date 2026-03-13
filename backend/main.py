from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, equipment, quotation, service_order, customer_order, customer, lab_service, calendar, users
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.user import Role
from fastapi.responses import JSONResponse
import traceback
import os
from sqlalchemy import text

# --- cPanel/WSGI Initialization ---
def init_db():
    if os.getenv("TESTING") == "True":
        return
        
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize Roles
    db = SessionLocal()
    try:
        roles = ["Admin", "Tecnico", "Visor"]
        for role_name in roles:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                db.add(Role(name=role_name))
        db.commit()
    finally:
        db.close()

    # Column migrations
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
    for i in range(1, 15):
        columns_to_add.append((f"criteria_{i}", "BOOLEAN DEFAULT TRUE"))

    with engine.connect() as conn:
        for col_name, col_type in columns_to_add:
            try:
                conn.execute(text(f"ALTER TABLE equipos ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
            except Exception as e:
                print(f"Error checking column {col_name} in equipos: {e}")
        
        calib_cols = [("empresa_certificadora", "VARCHAR"), ("certificado_url", "VARCHAR")]
        for col_name, col_type in calib_cols:
            try:
                conn.execute(text(f"ALTER TABLE calibraciones ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
            except Exception:
                pass
        
        try:
            conn.execute(text("ALTER TABLE lab_services ADD COLUMN IF NOT EXISTS norm VARCHAR"))
        except Exception as e:
            print(f"Error checking column norm in lab_services: {e}")
        
        conn.commit()

# Call initialization directly
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Laboratorio de Suelos API", lifespan=lifespan)

# --- Error Hunter ---
@app.exception_handler(Exception)
async def debug_exception_handler(request, exc):
    origin = os.getenv("CORS_ORIGINS", "http://localhost:5032") 
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "trace": traceback.format_exc()},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true"
        }
    )

# --- CORS Configuration ---
origins = [
    "http://localhost:5032",
    "https://laboratoriolsmch.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/usuarios", tags=["usuarios"])
app.include_router(equipment.router, prefix="/api/equipos", tags=["equipos"])
app.include_router(quotation.router, prefix="/api/cotizaciones", tags=["cotizaciones"])
app.include_router(service_order.router, prefix="/api/ordenes-servicio", tags=["ordenes_servicio"])
app.include_router(customer_order.router, prefix="/api/pedidos", tags=["pedidos"])
app.include_router(customer.router, prefix="/api/clientes", tags=["clientes"])
app.include_router(lab_service.router, prefix="/api/servicios", tags=["servicios"])
app.include_router(calendar.router, prefix="/api/agenda", tags=["agenda"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Laboratorio de Suelos"}
