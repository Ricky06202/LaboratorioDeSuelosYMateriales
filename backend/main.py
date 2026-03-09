from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, equipment, quotation, service_order, customer_order
from app.db.session import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
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
        ("ubicacion_fisica", "VARCHAR")
    ]
    with engine.connect() as conn:
        for col_name, col_type in columns_to_add:
            try:
                # Add columns if they don't exist
                conn.execute(text(f"ALTER TABLE equipos ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                print(f"Verified/Added column {col_name} to equipos table")
            except Exception as e:
                print(f"Error checking column {col_name}: {e}")
        conn.commit()
    yield

app = FastAPI(title="Laboratorio de Suelos API", lifespan=lifespan)

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
