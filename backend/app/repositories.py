from __future__ import annotations

"""Persistência: único ponto com consultas SQLAlchemy."""
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import SCHEDULED, Appointment, Client, Service


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, q: str | None = None) -> list[Client]:
        stmt = select(Client).order_by(Client.name)
        if q:
            like = f"%{q.strip().lower()}%"
            stmt = stmt.where(func.lower(Client.name).like(like) | func.lower(Client.email).like(like))
        return list(self.db.scalars(stmt))

    def get(self, id_: int) -> Client | None:
        return self.db.get(Client, id_)

    def get_by_email(self, email: str) -> Client | None:
        return self.db.scalar(select(Client).where(Client.email == email))

    def add(self, obj: Client) -> Client:
        self.db.add(obj)
        self.db.flush()
        return obj

    def delete(self, obj: Client) -> None:
        self.db.delete(obj)
        self.db.flush()

    def count(self) -> int:
        return self.db.scalar(select(func.count(Client.id))) or 0


class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Service]:
        return list(self.db.scalars(select(Service).order_by(Service.name)))

    def get(self, id_: int) -> Service | None:
        return self.db.get(Service, id_)

    def get_by_name(self, name: str) -> Service | None:
        return self.db.scalar(select(Service).where(func.lower(Service.name) == name.lower()))

    def add(self, obj: Service) -> Service:
        self.db.add(obj)
        self.db.flush()
        return obj

    def delete(self, obj: Service) -> None:
        self.db.delete(obj)
        self.db.flush()

    def count(self) -> int:
        return self.db.scalar(select(func.count(Service.id))) or 0


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, date_from=None, date_to=None, status=None, client_id=None) -> list[Appointment]:
        stmt = select(Appointment).order_by(Appointment.start_at)
        if date_from:
            stmt = stmt.where(Appointment.start_at >= date_from)
        if date_to:
            stmt = stmt.where(Appointment.start_at < date_to)
        if status:
            stmt = stmt.where(Appointment.status == status)
        if client_id:
            stmt = stmt.where(Appointment.client_id == client_id)
        return list(self.db.scalars(stmt).unique())

    def get(self, id_: int) -> Appointment | None:
        return self.db.get(Appointment, id_)

    def find_conflict(self, start: datetime, end: datetime, exclude_id: int | None = None) -> Appointment | None:
        stmt = select(Appointment).where(
            Appointment.status == SCHEDULED,
            Appointment.start_at < end,
            Appointment.end_at > start,
        )
        if exclude_id is not None:
            stmt = stmt.where(Appointment.id != exclude_id)
        return self.db.scalars(stmt).unique().first()

    def add(self, obj: Appointment) -> Appointment:
        self.db.add(obj)
        self.db.flush()
        return obj

    def delete(self, obj: Appointment) -> None:
        self.db.delete(obj)
        self.db.flush()

    def exists_for_client(self, client_id: int, only_scheduled: bool = False) -> bool:
        stmt = select(func.count(Appointment.id)).where(Appointment.client_id == client_id)
        if only_scheduled:
            stmt = stmt.where(Appointment.status == SCHEDULED)
        return (self.db.scalar(stmt) or 0) > 0

    def exists_for_service(self, service_id: int) -> bool:
        stmt = select(func.count(Appointment.id)).where(Appointment.service_id == service_id)
        return (self.db.scalar(stmt) or 0) > 0

    def count_status_between(self, status: str, start: datetime | None = None, end: datetime | None = None) -> int:
        stmt = select(func.count(Appointment.id)).where(Appointment.status == status)
        if start:
            stmt = stmt.where(Appointment.start_at >= start)
        if end:
            stmt = stmt.where(Appointment.start_at < end)
        return self.db.scalar(stmt) or 0

    def expected_revenue(self, start: datetime) -> float:
        stmt = (
            select(func.coalesce(func.sum(Service.price), 0.0))
            .select_from(Appointment)
            .join(Service, Service.id == Appointment.service_id)
            .where(Appointment.status == SCHEDULED, Appointment.start_at >= start)
        )
        return float(self.db.scalar(stmt) or 0.0)

    def upcoming(self, start: datetime, limit: int) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .where(Appointment.status == SCHEDULED, Appointment.start_at >= start)
            .order_by(Appointment.start_at)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).unique())
