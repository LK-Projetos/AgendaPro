"""Regras de negócio. Não conhece HTTP; usa repositórios."""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import repositories as repo
from .errors import BusinessRuleError, ConflictError, NotFoundError, ScheduleConflictError
from .models import CANCELLED, SCHEDULED, Appointment, Client, Service
from .schemas import AppointmentIn, ClientIn, ServiceIn


def now() -> datetime:
    """Relógio isolado para permitir teste determinístico."""
    return datetime.now().replace(second=0, microsecond=0)


# ---------------- Clientes ----------------
class ClientService:
    def __init__(self, db: Session):
        self.db = db
        self.clients = repo.ClientRepository(db)
        self.appointments = repo.AppointmentRepository(db)

    def list(self, q: str | None = None):
        return self.clients.list(q)

    def get(self, id_: int) -> Client:
        obj = self.clients.get(id_)
        if not obj:
            raise NotFoundError("Cliente não encontrado.")
        return obj

    def _check_email(self, email: str, own_id: int | None = None):
        other = self.clients.get_by_email(email)
        if other and other.id != own_id:
            raise ConflictError("Já existe um cliente com este e-mail.", {"field": "email"})

    def create(self, data: ClientIn) -> Client:
        self._check_email(data.email)
        obj = self.clients.add(Client(**data.model_dump()))
        self.db.commit()
        return obj

    def update(self, id_: int, data: ClientIn) -> Client:
        obj = self.get(id_)
        self._check_email(data.email, id_)
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        self.db.commit()
        return obj

    def delete(self, id_: int) -> None:
        obj = self.get(id_)
        if self.appointments.exists_for_client(id_):
            raise ConflictError("Cliente possui agendamentos. Exclua ou cancele-os antes de remover o cliente.")
        self.clients.delete(obj)
        self.db.commit()


# ---------------- Serviços ----------------
class ServiceService:
    def __init__(self, db: Session):
        self.db = db
        self.services = repo.ServiceRepository(db)
        self.appointments = repo.AppointmentRepository(db)

    def list(self):
        return self.services.list()

    def get(self, id_: int) -> Service:
        obj = self.services.get(id_)
        if not obj:
            raise NotFoundError("Serviço não encontrado.")
        return obj

    def _check_name(self, name: str, own_id: int | None = None):
        other = self.services.get_by_name(name)
        if other and other.id != own_id:
            raise ConflictError("Já existe um serviço com este nome.", {"field": "name"})

    def create(self, data: ServiceIn) -> Service:
        self._check_name(data.name)
        obj = self.services.add(Service(**data.model_dump()))
        self.db.commit()
        return obj

    def update(self, id_: int, data: ServiceIn) -> Service:
        obj = self.get(id_)
        self._check_name(data.name, id_)
        for k, v in data.model_dump().items():
            setattr(obj, k, v)
        self.db.commit()  # agendamentos existentes mantêm seus horários já calculados
        return obj

    def delete(self, id_: int) -> None:
        obj = self.get(id_)
        if self.appointments.exists_for_service(id_):
            raise ConflictError("Serviço possui agendamentos e não pode ser excluído.")
        self.services.delete(obj)
        self.db.commit()


# ---------------- Agendamentos ----------------
class AppointmentService:
    def __init__(self, db: Session):
        self.db = db
        self.appointments = repo.AppointmentRepository(db)
        self.clients = repo.ClientRepository(db)
        self.services = repo.ServiceRepository(db)

    def list(self, **filters):
        return self.appointments.list(**filters)

    def get(self, id_: int) -> Appointment:
        obj = self.appointments.get(id_)
        if not obj:
            raise NotFoundError("Agendamento não encontrado.")
        return obj

    def _validate_slot(self, start: datetime, end: datetime, exclude_id: int | None = None):
        if start < now():
            raise BusinessRuleError("Não é possível agendar em data/hora passada.", {"field": "start_at"})
        clash = self.appointments.find_conflict(start, end, exclude_id)
        if clash:
            raise ScheduleConflictError(
                "Horário indisponível: já existe um agendamento neste intervalo.",
                {
                    "conflict_id": clash.id,
                    "conflict_start": clash.start_at.isoformat(),
                    "conflict_end": clash.end_at.isoformat(),
                },
            )

    def _refs(self, client_id: int, service_id: int) -> tuple[Client, Service]:
        client = self.clients.get(client_id)
        if not client:
            raise BusinessRuleError("Cliente informado não existe.", {"field": "client_id"})
        service = self.services.get(service_id)
        if not service:
            raise BusinessRuleError("Serviço informado não existe.", {"field": "service_id"})
        return client, service

    def create(self, data: AppointmentIn) -> Appointment:
        _, service = self._refs(data.client_id, data.service_id)
        end = data.start_at + timedelta(minutes=service.duration_minutes)
        self._validate_slot(data.start_at, end)
        obj = self.appointments.add(
            Appointment(
                client_id=data.client_id,
                service_id=data.service_id,
                start_at=data.start_at,
                end_at=end,
                status=SCHEDULED,
                notes=data.notes,
            )
        )
        self.db.commit()
        return obj

    def update(self, id_: int, data: AppointmentIn) -> Appointment:
        obj = self.get(id_)
        if obj.status == CANCELLED:
            raise ConflictError("Agendamento cancelado não pode ser editado.")
        _, service = self._refs(data.client_id, data.service_id)
        end = data.start_at + timedelta(minutes=service.duration_minutes)
        if data.start_at != obj.start_at or end != obj.end_at:
            self._validate_slot(data.start_at, end, exclude_id=id_)
        obj.client_id, obj.service_id = data.client_id, data.service_id
        obj.start_at, obj.end_at, obj.notes = data.start_at, end, data.notes
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def reschedule(self, id_: int, start: datetime) -> Appointment:
        obj = self.get(id_)
        if obj.status != SCHEDULED:
            raise ConflictError("Só é possível remarcar agendamentos ativos.")
        duration = obj.end_at - obj.start_at
        self._validate_slot(start, start + duration, exclude_id=id_)
        obj.start_at, obj.end_at = start, start + duration
        self.db.commit()
        return obj

    def cancel(self, id_: int) -> Appointment:
        obj = self.get(id_)
        if obj.status == CANCELLED:
            raise ConflictError("Agendamento já está cancelado.")
        obj.status = CANCELLED
        self.db.commit()
        return obj

    def delete(self, id_: int) -> None:
        obj = self.get(id_)
        self.appointments.delete(obj)
        self.db.commit()


# ---------------- Dashboard ----------------
class DashboardService:
    def __init__(self, db: Session):
        self.appointments = repo.AppointmentRepository(db)
        self.clients = repo.ClientRepository(db)
        self.services = repo.ServiceRepository(db)

    def summary(self) -> dict:
        n = now()
        today = n.replace(hour=0, minute=0)
        scheduled = self.appointments.count_status_between(SCHEDULED)
        cancelled = self.appointments.count_status_between(CANCELLED)
        total = scheduled + cancelled
        return {
            "total_clients": self.clients.count(),
            "total_services": self.services.count(),
            "today_count": self.appointments.count_status_between(SCHEDULED, today, today + timedelta(days=1)),
            "next7_count": self.appointments.count_status_between(SCHEDULED, n, n + timedelta(days=7)),
            "scheduled_total": scheduled,
            "cancelled_total": cancelled,
            "cancellation_rate": round(cancelled / total * 100, 1) if total else 0.0,
            "expected_revenue": round(self.appointments.expected_revenue(n), 2),
            "next_appointments": self.appointments.upcoming(n, 5),
        }
