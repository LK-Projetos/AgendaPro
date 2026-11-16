"""Dados FICTÍCIOS de demonstração. Uso: python -m app.seed
Não apaga nada: se o banco já tiver dados, não faz nada."""
from datetime import datetime, timedelta

from .database import Base, SessionLocal, engine
from .models import CANCELLED, SCHEDULED, Appointment, Client, Service

CLIENTS = [
    ("Ana Exemplo", "ana@exemplo.test", "11999990001"),
    ("Bruno Teste", "bruno@exemplo.test", "11999990002"),
    ("Carla Demo", "carla@exemplo.test", "21999990003"),
    ("Diego Fictício", "diego@exemplo.test", "31999990004"),
    ("Elisa Modelo", "elisa@exemplo.test", "41999990005"),
    ("Fábio Amostra", "fabio@exemplo.test", "51999990006"),
]
SERVICES = [
    ("Corte de cabelo", "Corte simples", 30, 50.0),
    ("Barba", "Barba completa", 30, 35.0),
    ("Corte + Barba", "Combo", 60, 80.0),
    ("Coloração", "Coloração completa", 120, 180.0),
]


def run() -> str:
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.query(Client).count() or db.query(Service).count():
            return "Banco já possui dados; seed ignorado."
        clients = [Client(name=n, email=e, phone=p) for n, e, p in CLIENTS]
        services = [Service(name=n, description=d, duration_minutes=m, price=p) for n, d, m, p in SERVICES]
        db.add_all(clients + services)
        db.flush()
        base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        plan = [  # (dias, hora, minuto, cliente, serviço, status)
            (-3, 9, 0, 0, 0, SCHEDULED),
            (-2, 14, 0, 1, 2, SCHEDULED),
            (-1, 10, 0, 2, 3, CANCELLED),
            (0, 18, 0, 3, 1, SCHEDULED),
            (0, 19, 0, 4, 0, SCHEDULED),
            (1, 9, 0, 0, 2, SCHEDULED),
            (1, 11, 0, 5, 3, SCHEDULED),
            (2, 15, 0, 1, 0, CANCELLED),
            (3, 10, 30, 2, 1, SCHEDULED),
            (5, 16, 0, 3, 2, SCHEDULED),
        ]
        for d, h, m, ci, si, st in plan:
            start = base + timedelta(days=d, hours=h, minutes=m)
            db.add(
                Appointment(
                    client_id=clients[ci].id,
                    service_id=services[si].id,
                    start_at=start,
                    end_at=start + timedelta(minutes=services[si].duration_minutes),
                    status=st,
                )
            )
        db.commit()
    return "Seed concluído (6 clientes, 4 serviços, 10 agendamentos fictícios)."


if __name__ == "__main__":
    print(run())
