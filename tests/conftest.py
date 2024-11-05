import pytest
<<<<<<< HEAD
=======
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
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_db
from app.main import app

<<<<<<< HEAD
# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
=======
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
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Creates a new database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Creates a new FastAPI TestClient."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
<<<<<<< HEAD
    return TestClient(app) 
=======
    with TestClient(app) as c:
        yield c
>>>>>>> be5220edfd9c10ca47d60657c71d9ee5d1c8aeee
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
