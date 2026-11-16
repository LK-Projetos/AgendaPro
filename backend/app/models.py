"""Entidades persistidas (camada de modelo)."""
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

SCHEDULED = "SCHEDULED"
CANCELLED = "CANCELLED"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    phone: Mapped[str] = mapped_column(String(15))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Service(Base):
    __tablename__ = "services"
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_service_duration"),
        CheckConstraint("price >= 0", name="ck_service_price"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        CheckConstraint("end_at > start_at", name="ck_appointment_range"),
        CheckConstraint("status IN ('SCHEDULED','CANCELLED')", name="ck_appointment_status"),
        Index("ix_appointments_range", "start_at", "end_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(12), default=SCHEDULED)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    client: Mapped[Client] = relationship(lazy="joined")
    service: Mapped[Service] = relationship(lazy="joined")
