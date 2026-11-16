from .conftest import make_appt


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


# ---------- clientes ----------
def test_client_crud(client):
    r = client.post("/api/clients", json={"name": " Bia Teste ", "email": "BIA@T.test", "phone": "(21) 98888-7777"})
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Bia Teste" and body["email"] == "bia@t.test" and body["phone"] == "21988887777"
    cid = body["id"]
    assert client.get(f"/api/clients/{cid}").json()["name"] == "Bia Teste"
    r = client.put(f"/api/clients/{cid}", json={"name": "Bia Nova", "email": "bia@t.test", "phone": "2188887777"})
    assert r.status_code == 200 and r.json()["name"] == "Bia Nova"
    assert len(client.get("/api/clients?q=nova").json()) == 1
    assert client.get("/api/clients?q=zzz").json() == []
    assert client.delete(f"/api/clients/{cid}").status_code == 204
    assert client.get(f"/api/clients/{cid}").status_code == 404


def test_client_validation(client):
    r = client.post("/api/clients", json={"name": "A", "email": "x", "phone": "123"})
    assert r.status_code == 422
    body = r.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert set(body["details"]["fields"]) == {"name", "email", "phone"}


def test_client_duplicate_email(client):
    data = {"name": "Dup Um", "email": "d@t.test", "phone": "11999990000"}
    assert client.post("/api/clients", json=data).status_code == 201
    r = client.post("/api/clients", json={**data, "name": "Dup Dois"})
    assert r.status_code == 409 and r.json()["code"] == "CONFLICT"


def test_client_update_same_email_ok_other_email_conflict(client):
    a = client.post("/api/clients", json={"name": "Aa Aa", "email": "a@t.test", "phone": "11999990000"}).json()
    client.post("/api/clients", json={"name": "Bb Bb", "email": "b@t.test", "phone": "11999990001"})
    ok = client.put(f"/api/clients/{a['id']}", json={"name": "Aa Novo", "email": "a@t.test", "phone": "11999990000"})
    assert ok.status_code == 200
    bad = client.put(f"/api/clients/{a['id']}", json={"name": "Aa Novo", "email": "b@t.test", "phone": "11999990000"})
    assert bad.status_code == 409


def test_client_not_found(client):
    assert client.get("/api/clients/999").status_code == 404
    assert client.delete("/api/clients/999").json()["code"] == "NOT_FOUND"


def test_client_with_appointments_cannot_be_deleted(client, seed):
    assert make_appt(client, seed).status_code == 201
    r = client.delete(f"/api/clients/{seed['client']['id']}")
    assert r.status_code == 409


# ---------- serviços ----------
def test_service_crud(client):
    r = client.post("/api/services", json={"name": "Massagem", "description": " Relaxante ", "duration_minutes": 45, "price": 99.999})
    assert r.status_code == 201
    s = r.json()
    assert s["price"] == 100.0 and s["description"] == "Relaxante"
    r = client.put(f"/api/services/{s['id']}", json={"name": "Massagem", "duration_minutes": 60, "price": 120})
    assert r.status_code == 200 and r.json()["duration_minutes"] == 60
    assert len(client.get("/api/services").json()) == 1
    assert client.delete(f"/api/services/{s['id']}").status_code == 204
    assert client.get(f"/api/services/{s['id']}").status_code == 404


def test_service_validation(client):
    for bad in (
        {"name": "X", "duration_minutes": 30, "price": 10},
        {"name": "Ok Nome", "duration_minutes": 20, "price": 10},
        {"name": "Ok Nome", "duration_minutes": 0, "price": 10},
        {"name": "Ok Nome", "duration_minutes": 30, "price": -1},
    ):
        r = client.post("/api/services", json=bad)
        assert r.status_code == 422, bad


def test_service_duplicate_name_case_insensitive(client):
    client.post("/api/services", json={"name": "Corte", "duration_minutes": 30, "price": 10})
    r = client.post("/api/services", json={"name": "corte", "duration_minutes": 30, "price": 10})
    assert r.status_code == 409


def test_service_with_appointments_cannot_be_deleted(client, seed):
    make_appt(client, seed)
    assert client.delete(f"/api/services/{seed['s30']['id']}").status_code == 409
