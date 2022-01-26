import pytest 

from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from .main import app, get_db
from .models import Commerce, Employee
from .database import Base
from requests.auth import HTTPBasicAuth

client = TestClient(app)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app) 
    yield client
    app.dependency_overrides.clear()


class TestMainClass():

    def set_commerce_auth(self, session: Session):
        self.commerce = Commerce(name='test', email='test@test', phone='134565432', api_key='test')
        session.add(self.commerce)
        session.commit()
        self.auth = HTTPBasicAuth(username="test", password="test")

    def test_get_employees(self, session: Session, client: TestClient):
        self.set_commerce_auth(session)
        emp1 = Employee(name='Joe', last_name="Doe", pin="1234", commerce_id=self.commerce.id)
        emp2 = Employee(name='Karen', last_name="Smith", pin="4321", commerce_id=self.commerce.id)
        session.add(emp1)
        session.add(emp2)
        session.commit()

        response = client.get("/employees", auth=self.auth)

        data = response.json()['data']
        assert response.status_code == 200
        assert len(data) == 2
        assert all(k in data[0] for k in ("active", "created_on", "full_name", "id", "pin"))

    def test_get_employee(self, session: Session, client: TestClient):
        self.set_commerce_auth(session)
        emp1 = Employee(name='Joe', last_name="Doe", pin="1234", commerce_id=self.commerce.id, uuid='12test12')
        session.add(emp1)
        session.commit()

        response = client.get(f"/employees/{emp1.uuid}", auth=self.auth)

        data = response.json()['data']
        assert response.status_code == 200
        assert len(data) == 5
        assert data['full_name'] == "Joe Doe"

    def test_create_employee(self, session: Session, client: TestClient):
        self.set_commerce_auth(session)
        emp1 = Employee(name='Joe', last_name="Doe", pin="1234", commerce_id=self.commerce.id, uuid='12test12')
        session.add(emp1)
        session.commit()
        
        response = client.post(f"/employees/", auth=self.auth, json={"name": "Dave", "last_name": "Wilson", "pin": "89765"})
        assert response.status_code == 200
        data = response.json()['data']
        assert len(data) == 5
        assert data['full_name'] == "Dave Wilson"
        

    def test_update_employee(self, session: Session, client: TestClient):
        self.set_commerce_auth(session)
        emp1 = Employee(name='Joe', last_name="Doe", pin="1234", commerce_id=self.commerce.id, uuid='12test12')
        session.add(emp1)
        session.commit()
        
        response = client.put(f"/employees/{emp1.uuid}", auth=self.auth, json={"name": "Joe", "last_name": "Wilson", "active": 1, "pin": "1234"})
        assert response.status_code == 200
        data = response.json()['data']
        assert len(data) == 5
        assert data['full_name'] == "Joe Wilson"

    def test_delete_employee(self, session: Session, client: TestClient):
        self.set_commerce_auth(session)
        emp1 = Employee(name='Joe', last_name="Doe", pin="1234", commerce_id=self.commerce.id, uuid='12test12')
        session.add(emp1)
        session.commit()
        
        response = client.delete(f"/employees/{emp1.uuid}", auth=self.auth)
        assert response.status_code == 200
        data = response.json()['data']
        assert len(data) == 0