import pytest
<<<<<<< HEAD
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base  # Updated import
from app.db.session import get_db
from app.main import app

warnings.filterwarnings(
    "ignore",
    message="datetime.datetime.utcnow()",
    category=DeprecationWarning
)

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/fastapi_test_db"
=======
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

SQLALCHEMY_DATABASE_URL = 'mysql://root:@localhost:3306/fastapi_test_db'
>>>>>>> be5220edfd9c10ca47d60657c71d9ee5d1c8aeee

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

<<<<<<< HEAD
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def test_db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    def override_get_db():
        try:
            yield session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
=======
@pytest.fixture(scope='session')
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='module')
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
>>>>>>> be5220edfd9c10ca47d60657c71d9ee5d1c8aeee
