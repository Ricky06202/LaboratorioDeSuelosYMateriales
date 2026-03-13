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


# ==================== SHARED FIXTURES ====================

@pytest.fixture(scope="function")
def test_user(db):
    """Create a test user"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    user = User(
        email="testuser@test.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123"),
        phone="12345678",
        cell_phone="67890123",
        cedula="8-123-456",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def admin_user(db):
    """Create an admin user with admin role"""
    from app.models.user import User, Role
    from app.core.security import get_password_hash
    
    role = Role(name="Admin", id=1)
    db.add(role)
    db.commit()
    
    user = User(
        email="admin@test.com",
        full_name="Admin User",
        hashed_password=get_password_hash("adminpass123"),
        is_active=True
    )
    user.roles.append(role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_customer(db):
    """Create a test customer"""
    from app.models.customer import Customer
    
    customer = Customer(
        name="Test Customer",
        ruc="12345678901",
        dv="1",
        phone="12345678",
        email="customer@test.com",
        address="Test Address"
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@pytest.fixture(scope="function")
def test_lab_service(db):
    """Create a test lab service"""
    from app.models.lab_service import LabService
    
    service = LabService(
        code="TEST001",
        name="Test Service",
        description="Test Description",
        norm="ASTM D-422",
        unit_price=100.0
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
