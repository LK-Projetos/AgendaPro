"""Contratos de entrada e saída da API (validação)."""
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ClientIn(BaseModel):
    name: str
    email: str
    phone: str

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        v = v.strip()
        if not 2 <= len(v) <= 120:
            raise ValueError("Nome deve ter entre 2 e 120 caracteres.")
        return v

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) > 120 or not EMAIL_RE.match(v):
            raise ValueError("E-mail inválido.")
        return v

    @field_validator("phone")
    @classmethod
    def _phone(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if not 10 <= len(digits) <= 11:
            raise ValueError("Telefone deve ter 10 ou 11 dígitos (com DDD).")
        return digits


class ClientOut(ClientIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class ServiceIn(BaseModel):
    name: str
    description: str | None = None
    duration_minutes: int
    price: float

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        v = v.strip()
        if not 2 <= len(v) <= 100:
            raise ValueError("Nome deve ter entre 2 e 100 caracteres.")
        return v

    @field_validator("description")
    @classmethod
    def _desc(cls, v: str | None) -> str | None:
        v = (v or "").strip()
        return v or None

    @field_validator("duration_minutes")
    @classmethod
    def _dur(cls, v: int) -> int:
        if not 15 <= v <= 480 or v % 15:
            raise ValueError("Duração deve estar entre 15 e 480 minutos, em múltiplos de 15.")
        return v

    @field_validator("price")
    @classmethod
    def _price(cls, v: float) -> float:
        if v < 0 or v > 100000:
            raise ValueError("Preço deve estar entre 0 e 100000.")
        return round(v, 2)


class ServiceOut(ServiceIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


def normalize_start(v: datetime) -> datetime:
    v = v.replace(tzinfo=None, second=0, microsecond=0)  # horário local do estabelecimento
    if v.minute % 15:
        raise ValueError("O horário deve começar em múltiplos de 15 minutos.")
    return v


class AppointmentIn(BaseModel):
    client_id: int
    service_id: int
    start_at: datetime
    notes: str | None = None

    @field_validator("start_at")
    @classmethod
    def _start(cls, v: datetime) -> datetime:
        return normalize_start(v)

    @field_validator("notes")
    @classmethod
    def _notes(cls, v: str | None) -> str | None:
        v = (v or "").strip()
        if len(v) > 500:
            raise ValueError("Observações devem ter no máximo 500 caracteres.")
        return v or None


class RescheduleIn(BaseModel):
    start_at: datetime

    @field_validator("start_at")
    @classmethod
    def _start(cls, v: datetime) -> datetime:
        return normalize_start(v)


class ClientRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ServiceRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    duration_minutes: int
    price: float


class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    client: ClientRef
    service: ServiceRef
    start_at: datetime
    end_at: datetime
    status: str
    notes: str | None


class DashboardOut(BaseModel):
    total_clients: int
    total_services: int
    today_count: int
    next7_count: int
    scheduled_total: int
    cancelled_total: int
    cancellation_rate: float
    expected_revenue: float
    next_appointments: list[AppointmentOut]
