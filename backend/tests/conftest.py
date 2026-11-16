from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import services
from app.database import Base, get_db, make_engine
from app.main import app

FIXED_NOW = datetime(2030, 1, 7, 8, 0)  # segunda-feira, relógio congelado nos testes


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(services, "now", lambda: FIXED_NOW)
    engine = make_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture()
def seed(client):
    """Cria 1 cliente e 2 serviços (30 e 60 min) via API."""
    c = client.post("/api/clients", json={"name": "Ana Teste", "email": "ana@t.test", "phone": "(11) 99999-0001"}).json()
    s30 = client.post("/api/services", json={"name": "Corte", "duration_minutes": 30, "price": 50}).json()
    s60 = client.post("/api/services", json={"name": "Combo", "duration_minutes": 60, "price": 80}).json()
    return {"client": c, "s30": s30, "s60": s60}


def make_appt(client, seed, start="2030-01-08T10:00", service="s30", **extra):
    return client.post(
        "/api/appointments",
        json={"client_id": seed["client"]["id"], "service_id": seed[service]["id"], "start_at": start, **extra},
    )
