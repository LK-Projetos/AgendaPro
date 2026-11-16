"""Rotas HTTP (controllers). Sem regra de negócio."""
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..errors import BusinessRuleError
from ..schemas import (
    AppointmentIn,
    AppointmentOut,
    ClientIn,
    ClientOut,
    DashboardOut,
    RescheduleIn,
    ServiceIn,
    ServiceOut,
)
from ..services import AppointmentService, ClientService, DashboardService, ServiceService

router = APIRouter(prefix="/api")


@router.get("/health", tags=["sistema"])
def health():
    return {"status": "ok"}


@router.get("/dashboard", response_model=DashboardOut, tags=["dashboard"])
def dashboard(db: Session = Depends(get_db)):
    return DashboardService(db).summary()


# ----- clientes -----
@router.get("/clients", response_model=list[ClientOut], tags=["clientes"])
def list_clients(q: str | None = None, db: Session = Depends(get_db)):
    return ClientService(db).list(q)


@router.post("/clients", response_model=ClientOut, status_code=201, tags=["clientes"])
def create_client(data: ClientIn, db: Session = Depends(get_db)):
    return ClientService(db).create(data)


@router.get("/clients/{id_}", response_model=ClientOut, tags=["clientes"])
def get_client(id_: int, db: Session = Depends(get_db)):
    return ClientService(db).get(id_)


@router.put("/clients/{id_}", response_model=ClientOut, tags=["clientes"])
def update_client(id_: int, data: ClientIn, db: Session = Depends(get_db)):
    return ClientService(db).update(id_, data)


@router.delete("/clients/{id_}", status_code=204, tags=["clientes"])
def delete_client(id_: int, db: Session = Depends(get_db)):
    ClientService(db).delete(id_)
    return Response(status_code=204)


# ----- serviços -----
@router.get("/services", response_model=list[ServiceOut], tags=["serviços"])
def list_services(db: Session = Depends(get_db)):
    return ServiceService(db).list()


@router.post("/services", response_model=ServiceOut, status_code=201, tags=["serviços"])
def create_service(data: ServiceIn, db: Session = Depends(get_db)):
    return ServiceService(db).create(data)


@router.get("/services/{id_}", response_model=ServiceOut, tags=["serviços"])
def get_service(id_: int, db: Session = Depends(get_db)):
    return ServiceService(db).get(id_)


@router.put("/services/{id_}", response_model=ServiceOut, tags=["serviços"])
def update_service(id_: int, data: ServiceIn, db: Session = Depends(get_db)):
    return ServiceService(db).update(id_, data)


@router.delete("/services/{id_}", status_code=204, tags=["serviços"])
def delete_service(id_: int, db: Session = Depends(get_db)):
    ServiceService(db).delete(id_)
    return Response(status_code=204)


# ----- agendamentos -----
@router.get("/appointments", response_model=list[AppointmentOut], tags=["agendamentos"])
def list_appointments(
    date_from: date | None = None,
    date_to: date | None = None,
    status: str | None = Query(None, pattern="^(SCHEDULED|CANCELLED)$"),
    client_id: int | None = None,
    db: Session = Depends(get_db),
):
    if date_from and date_to and date_to < date_from:
        raise BusinessRuleError("Data final anterior à data inicial.")
    return AppointmentService(db).list(
        date_from=datetime.combine(date_from, datetime.min.time()) if date_from else None,
        date_to=datetime.combine(date_to + timedelta(days=1), datetime.min.time()) if date_to else None,
        status=status,
        client_id=client_id,
    )


@router.post("/appointments", response_model=AppointmentOut, status_code=201, tags=["agendamentos"])
def create_appointment(data: AppointmentIn, db: Session = Depends(get_db)):
    return AppointmentService(db).create(data)


@router.get("/appointments/{id_}", response_model=AppointmentOut, tags=["agendamentos"])
def get_appointment(id_: int, db: Session = Depends(get_db)):
    return AppointmentService(db).get(id_)


@router.put("/appointments/{id_}", response_model=AppointmentOut, tags=["agendamentos"])
def update_appointment(id_: int, data: AppointmentIn, db: Session = Depends(get_db)):
    return AppointmentService(db).update(id_, data)


@router.post("/appointments/{id_}/reschedule", response_model=AppointmentOut, tags=["agendamentos"])
def reschedule_appointment(id_: int, data: RescheduleIn, db: Session = Depends(get_db)):
    return AppointmentService(db).reschedule(id_, data.start_at)


@router.post("/appointments/{id_}/cancel", response_model=AppointmentOut, tags=["agendamentos"])
def cancel_appointment(id_: int, db: Session = Depends(get_db)):
    return AppointmentService(db).cancel(id_)


@router.delete("/appointments/{id_}", status_code=204, tags=["agendamentos"])
def delete_appointment(id_: int, db: Session = Depends(get_db)):
    AppointmentService(db).delete(id_)
    return Response(status_code=204)
