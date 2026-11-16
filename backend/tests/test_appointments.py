from .conftest import make_appt


def test_create_computes_end_and_lists(client, seed):
    r = make_appt(client, seed, "2030-01-08T10:00", "s60", notes=" teste ")
    assert r.status_code == 201
    a = r.json()
    assert a["end_at"] == "2030-01-08T11:00:00" and a["status"] == "SCHEDULED" and a["notes"] == "teste"
    assert a["client"]["name"] == "Ana Teste" and a["service"]["name"] == "Combo"
    assert len(client.get("/api/appointments").json()) == 1
    assert client.get(f"/api/appointments/{a['id']}").status_code == 200


def test_conflict_overlaps_rejected(client, seed):
    assert make_appt(client, seed, "2030-01-08T10:00", "s60").status_code == 201  # 10:00-11:00
    for start in ("2030-01-08T10:00", "2030-01-08T10:30", "2030-01-08T09:45"):
        r = make_appt(client, seed, start, "s30")
        assert r.status_code == 409, start
        assert r.json()["code"] == "SCHEDULE_CONFLICT"
    assert len(client.get("/api/appointments").json()) == 1


def test_adjacent_is_allowed(client, seed):
    assert make_appt(client, seed, "2030-01-08T10:00", "s60").status_code == 201
    assert make_appt(client, seed, "2030-01-08T11:00", "s30").status_code == 201  # começa quando o outro termina
    assert make_appt(client, seed, "2030-01-08T09:30", "s30").status_code == 201  # termina quando o outro começa


def test_cancelled_does_not_block(client, seed):
    a = make_appt(client, seed, "2030-01-08T10:00").json()
    assert client.post(f"/api/appointments/{a['id']}/cancel").json()["status"] == "CANCELLED"
    assert make_appt(client, seed, "2030-01-08T10:00").status_code == 201


def test_past_rejected(client, seed):
    r = make_appt(client, seed, "2030-01-07T07:45")
    assert r.status_code == 422 and r.json()["code"] == "BUSINESS_RULE"


def test_validation_and_references(client, seed):
    assert make_appt(client, seed, "2030-01-08T10:10").status_code == 422  # não múltiplo de 15
    r = client.post("/api/appointments", json={"client_id": 999, "service_id": seed["s30"]["id"], "start_at": "2030-01-08T10:00"})
    assert r.status_code == 422
    r = client.post("/api/appointments", json={"client_id": seed["client"]["id"], "service_id": 999, "start_at": "2030-01-08T10:00"})
    assert r.status_code == 422
    assert client.post("/api/appointments", json={}).json()["code"] == "VALIDATION_ERROR"
    assert client.post("/api/appointments", json={"client_id": 1, "service_id": 1, "start_at": "ontem"}).status_code == 422


def test_reschedule_ok_and_conflict_keeps_original(client, seed):
    a = make_appt(client, seed, "2030-01-08T10:00", "s60").json()
    b = make_appt(client, seed, "2030-01-08T14:00", "s30").json()
    r = client.post(f"/api/appointments/{a['id']}/reschedule", json={"start_at": "2030-01-08T10:30"})
    assert r.status_code == 200  # sobrepõe apenas a si mesmo
    assert r.json()["start_at"] == "2030-01-08T10:30:00" and r.json()["end_at"] == "2030-01-08T11:30:00"
    r = client.post(f"/api/appointments/{a['id']}/reschedule", json={"start_at": "2030-01-08T13:45"})
    assert r.status_code == 409
    again = client.get(f"/api/appointments/{a['id']}").json()
    assert again["start_at"] == "2030-01-08T10:30:00"
    assert b["id"] != a["id"]


def test_reschedule_cancelled_and_past_rejected(client, seed):
    a = make_appt(client, seed).json()
    assert client.post(f"/api/appointments/{a['id']}/reschedule", json={"start_at": "2030-01-01T10:00"}).status_code == 422
    client.post(f"/api/appointments/{a['id']}/cancel")
    assert client.post(f"/api/appointments/{a['id']}/reschedule", json={"start_at": "2030-01-09T10:00"}).status_code == 409


def test_cancel_twice_conflict_and_404(client, seed):
    a = make_appt(client, seed).json()
    assert client.post(f"/api/appointments/{a['id']}/cancel").status_code == 200
    assert client.post(f"/api/appointments/{a['id']}/cancel").status_code == 409
    assert client.post("/api/appointments/999/cancel").status_code == 404


def test_update_changes_service_recalculates_end_and_checks_conflict(client, seed):
    a = make_appt(client, seed, "2030-01-08T10:00", "s30").json()
    make_appt(client, seed, "2030-01-08T10:45", "s30")
    body = {"client_id": seed["client"]["id"], "service_id": seed["s60"]["id"], "start_at": "2030-01-08T10:00"}
    assert client.put(f"/api/appointments/{a['id']}", json=body).status_code == 409  # 10:00-11:00 bate com 10:45
    body["service_id"] = seed["s30"]["id"]
    body["notes"] = "só observação"
    r = client.put(f"/api/appointments/{a['id']}", json=body)
    assert r.status_code == 200 and r.json()["notes"] == "só observação"


def test_update_cancelled_rejected(client, seed):
    a = make_appt(client, seed).json()
    client.post(f"/api/appointments/{a['id']}/cancel")
    body = {"client_id": seed["client"]["id"], "service_id": seed["s30"]["id"], "start_at": "2030-01-08T10:00"}
    assert client.put(f"/api/appointments/{a['id']}", json=body).status_code == 409


def test_delete(client, seed):
    a = make_appt(client, seed).json()
    assert client.delete(f"/api/appointments/{a['id']}").status_code == 204
    assert client.get(f"/api/appointments/{a['id']}").status_code == 404
    assert client.delete(f"/api/appointments/{a['id']}").status_code == 404


def test_filters(client, seed):
    a = make_appt(client, seed, "2030-01-08T10:00").json()
    make_appt(client, seed, "2030-01-10T10:00")
    client.post(f"/api/appointments/{a['id']}/cancel")
    assert len(client.get("/api/appointments?status=CANCELLED").json()) == 1
    assert len(client.get("/api/appointments?date_from=2030-01-10&date_to=2030-01-10").json()) == 1
    assert len(client.get("/api/appointments?date_from=2030-01-08&date_to=2030-01-08").json()) == 1
    assert client.get("/api/appointments?status=XYZ").status_code == 422
    assert client.get("/api/appointments?date_from=2030-01-10&date_to=2030-01-08").status_code == 422
    assert len(client.get(f"/api/appointments?client_id={seed['client']['id']}").json()) == 2


def test_dashboard(client, seed):
    empty = client.get("/api/dashboard").json()
    assert empty["cancellation_rate"] == 0.0 and empty["expected_revenue"] == 0.0 and empty["next_appointments"] == []
    make_appt(client, seed, "2030-01-07T09:00", "s30")  # hoje, 50
    make_appt(client, seed, "2030-01-08T10:00", "s60")  # amanhã, 80
    c = make_appt(client, seed, "2030-01-20T10:00", "s30").json()  # fora dos 7 dias, 50
    cx = make_appt(client, seed, "2030-01-09T10:00", "s30").json()
    client.post(f"/api/appointments/{cx['id']}/cancel")
    d = client.get("/api/dashboard").json()
    assert d["total_clients"] == 1 and d["total_services"] == 2
    assert d["today_count"] == 1
    assert d["next7_count"] == 2
    assert d["scheduled_total"] == 3 and d["cancelled_total"] == 1
    assert d["cancellation_rate"] == 25.0
    assert d["expected_revenue"] == 180.0
    assert [x["start_at"] for x in d["next_appointments"]][0] == "2030-01-07T09:00:00"
    assert c["id"] in [x["id"] for x in d["next_appointments"]]
