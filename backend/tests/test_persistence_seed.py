"""Persistência real em arquivo SQLite (sobrevive a reinício) e seed."""
from sqlalchemy.orm import sessionmaker

from app import seed as seed_mod
from app.database import Base, make_engine
from app.models import Appointment, Client, Service


def test_data_survives_engine_restart(tmp_path):
    url = f"sqlite:///{(tmp_path / 'p.db').as_posix()}"
    e1 = make_engine(url)
    Base.metadata.create_all(e1)
    with sessionmaker(bind=e1)() as db:
        db.add(Client(name="Persistente", email="p@t.test", phone="11999990000"))
        db.commit()
    e1.dispose()  # "reinicia" a aplicação

    e2 = make_engine(url)
    with sessionmaker(bind=e2)() as db:
        assert db.query(Client).filter_by(email="p@t.test").one().name == "Persistente"
    e2.dispose()


def test_foreign_keys_enforced(tmp_path):
    import pytest
    from datetime import datetime
    from sqlalchemy.exc import IntegrityError

    e = make_engine(f"sqlite:///{(tmp_path / 'fk.db').as_posix()}")
    Base.metadata.create_all(e)
    with sessionmaker(bind=e)() as db:
        db.add(Appointment(client_id=1, service_id=1, start_at=datetime(2030, 1, 1, 9), end_at=datetime(2030, 1, 1, 10)))
        with pytest.raises(IntegrityError):
            db.commit()
    e.dispose()


def test_seed_creates_fake_data_and_is_idempotent(tmp_path, monkeypatch):
    e = make_engine(f"sqlite:///{(tmp_path / 's.db').as_posix()}")
    monkeypatch.setattr(seed_mod, "engine", e)
    monkeypatch.setattr(seed_mod, "SessionLocal", sessionmaker(bind=e, expire_on_commit=False))
    assert "concluído" in seed_mod.run()
    assert "ignorado" in seed_mod.run()
    with sessionmaker(bind=e)() as db:
        assert db.query(Client).count() == 6
        assert db.query(Service).count() == 4
        assert db.query(Appointment).count() == 10
        assert all(c.email.endswith("@exemplo.test") for c in db.query(Client))
    e.dispose()
