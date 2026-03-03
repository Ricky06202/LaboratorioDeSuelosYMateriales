from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, equipment
from app.db.session import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
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

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Laboratorio de Suelos"}
