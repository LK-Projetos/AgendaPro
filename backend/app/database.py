"""Configuração do banco SQLite e sessão SQLAlchemy."""
import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DEFAULT_DB = Path(__file__).resolve().parent.parent / "agendapro.db"
DATABASE_URL = os.environ.get("AGENDAPRO_DB_URL", f"sqlite:///{DEFAULT_DB.as_posix()}")


class Base(DeclarativeBase):
    pass


def make_engine(url: str = DATABASE_URL, **kwargs):
    engine = create_engine(url, connect_args={"check_same_thread": False}, **kwargs)

    @event.listens_for(engine, "connect")
    def _fk_on(dbapi_conn, _record):  # ativa chaves estrangeiras no SQLite
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()

    return engine


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
