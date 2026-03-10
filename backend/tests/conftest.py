import pytest
import os
import sys

# Add backend to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["TESTING"] = "True"

from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Mock Geometry for SQLite tests
import geoalchemy2
geoalchemy2.Geometry = lambda *args, **kwargs: String

from app.db.base_class import Base
from app.db.session import engine as prod_engine
from main import app
from app.api.deps import get_db
from app.models.equipment import Equipo, Calibracion  # Import models so Base sees them

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: cleanup test db file after session
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
