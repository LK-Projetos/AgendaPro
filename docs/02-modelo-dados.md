# Modelo de dados

## Diagrama de classes
```mermaid
classDiagram
  class Client { +int id; +string name; +string email; +string phone; +datetime created_at }
  class Service { +int id; +string name; +string description; +int duration_minutes; +float price }
  class Appointment {
    +int id; +datetime start_at; +datetime end_at; +string status; +string notes
    +datetime created_at; +datetime updated_at
  }
  class ClientService { list(); create(); update(); delete() }
  class ServiceService { list(); create(); update(); delete() }
  class AppointmentService { create(); update(); reschedule(); cancel(); delete(); -validate_slot() }
  class DashboardService { summary() }
  Client "1" --> "*" Appointment
  Service "1" --> "*" Appointment
  AppointmentService ..> Appointment
  ClientService ..> Client
  ServiceService ..> Service
  DashboardService ..> Appointment
```

## DER
```mermaid
erDiagram
  CLIENTS ||--o{ APPOINTMENTS : realiza
  SERVICES ||--o{ APPOINTMENTS : "é agendado em"
  CLIENTS { int id PK; string name; string email UK; string phone; datetime created_at }
  SERVICES { int id PK; string name UK; string description; int duration_minutes; float price }
  APPOINTMENTS { int id PK; int client_id FK; int service_id FK; datetime start_at; datetime end_at; string status; string notes; datetime created_at; datetime updated_at }
```

## Dicionário de dados
### clients
| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK | Identificador |
| name | VARCHAR(120) | NN, 2–120 chars (validação) | Nome |
| email | VARCHAR(120) | NN, UNIQUE | E-mail (minúsculas) |
| phone | VARCHAR(15) | NN, 10–11 dígitos (validação) | Telefone só dígitos |
| created_at | DATETIME | NN | Criação |

### services
| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK | |
| name | VARCHAR(100) | NN, UNIQUE | Nome |
| description | TEXT | nulo | |
| duration_minutes | INTEGER | NN, CHECK > 0 (+ regra 15–480, múltiplo de 15) | Duração |
| price | FLOAT | NN, CHECK ≥ 0 | Preço de referência (sem cobrança) |

### appointments
| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK | |
| client_id | INTEGER | FK clients.id, NN | |
| service_id | INTEGER | FK services.id, NN | |
| start_at | DATETIME | NN | Início (horário local) |
| end_at | DATETIME | NN, CHECK end_at > start_at | Início + duração |
| status | VARCHAR(12) | NN, CHECK in (SCHEDULED, CANCELLED) | |
| notes | TEXT | nulo, máx. 500 (validação) | |
| created_at, updated_at | DATETIME | NN | Auditoria |

Índice `ix_appointments_range (start_at, end_at)` para a consulta de conflito. Chaves estrangeiras ativadas com `PRAGMA foreign_keys=ON`.
