# Diagramas UML e ER (Mermaid)

Diagramas em Mermaid para serem versionados e renderizados no GitHub. Exportar para PNG/SVG para a entrega acadêmica, se exigido.

## 1. Casos de uso

```mermaid
flowchart LR
  Admin((Administrador))
  Cli((Cliente final))
  subgraph AgendaPro
    UC1[UC01 Autenticar]
    UC2[UC02 Visualizar dashboard]
    UC3[UC03 Gerenciar clientes]
    UC4[UC04 Gerenciar serviços]
    UC5[UC05 Gerenciar profissionais]
    UC6[UC06 Definir disponibilidade]
    UC7[UC07 Criar agendamento]
    UC8[UC08 Confirmar agendamento]
    UC9[UC09 Remarcar agendamento]
    UC10[UC10 Cancelar agendamento]
    UC11[UC11 Reservar horário online]
    UC12[UC12 Consultar horários livres]
    UC13[UC13 Validar conflito]
  end
  Admin --> UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC7 & UC8 & UC9 & UC10
  Cli --> UC11
  UC11 -. include .-> UC12
  UC11 -. include .-> UC13
  UC7 -. include .-> UC13
  UC9 -. include .-> UC13
  UC3 -. e UC4/UC5 exigem .-> UC1
```

| UC | Ator | Pré-condição | Fluxo principal | Alternativos |
|----|------|--------------|-----------------|--------------|
| UC07 | Admin | Autenticado; cliente, serviço, profissional existem | Seleciona cliente, serviço, profissional, data/hora → sistema calcula fim, valida → cria PENDING | Conflito → 409; fora da disponibilidade → 422 |
| UC11 | Cliente | Serviço ativo existe | Serviço → profissional → data → horário → dados → protocolo | Horário tomado → 409, volta à escolha |
| UC09 | Admin | Agendamento PENDING/CONFIRMED | Escolhe novo horário → valida → atualiza | Conflito → mantém original |

## 2. Diagrama de classes

```mermaid
classDiagram
  class User {
    +int id
    +string email
    +string passwordHash
    +string name
    +bool active
  }
  class Client {
    +int id
    +string name
    +string email
    +string phone
    +string notes
    +datetime createdAt
  }
  class Service {
    +int id
    +string name
    +string description
    +int durationMinutes
    +decimal price
    +bool active
  }
  class Professional {
    +int id
    +string name
    +string email
    +bool active
  }
  class Availability {
    +int id
    +int weekday
    +time startTime
    +time endTime
  }
  class Appointment {
    +int id
    +datetime startAt
    +datetime endAt
    +AppointmentStatus status
    +string notes
    +string protocol
    +string source
    +datetime createdAt
    +confirm()
    +reschedule(newStart)
    +cancel()
    +complete()
  }
  class AppointmentStatus {
    <<enumeration>>
    PENDING
    CONFIRMED
    CANCELLED
    COMPLETED
  }
  class AppointmentService {
    +create()
    +confirm()
    +reschedule()
    +cancel()
    -checkConflict()
    -checkAvailability()
  }
  class SlotService {
    +listFreeSlots(professional, service, date)
  }
  Professional "1" --> "*" Availability
  Professional "*" -- "*" Service : executa
  Client "1" --> "*" Appointment
  Professional "1" --> "*" Appointment
  Service "1" --> "*" Appointment
  Appointment --> AppointmentStatus
  AppointmentService ..> Appointment
  AppointmentService ..> SlotService
```

### Transições de status
```mermaid
stateDiagram-v2
  [*] --> PENDING
  PENDING --> CONFIRMED: confirmar
  PENDING --> CANCELLED: cancelar
  CONFIRMED --> CANCELLED: cancelar
  CONFIRMED --> COMPLETED: concluir
  PENDING --> PENDING: remarcar
  CONFIRMED --> CONFIRMED: remarcar
  CANCELLED --> [*]
  COMPLETED --> [*]
```

## 3. Entidade-relacionamento

```mermaid
erDiagram
  USERS {
    int id PK
    string email UK
    string password_hash
    string name
    bool active
  }
  CLIENTS {
    int id PK
    string name
    string email UK
    string phone
    string notes
    datetime created_at
  }
  SERVICES {
    int id PK
    string name UK
    string description
    int duration_minutes
    decimal price
    bool active
  }
  PROFESSIONALS {
    int id PK
    string name
    string email
    bool active
  }
  PROFESSIONAL_SERVICES {
    int professional_id PK,FK
    int service_id PK,FK
  }
  AVAILABILITIES {
    int id PK
    int professional_id FK
    int weekday
    time start_time
    time end_time
  }
  APPOINTMENTS {
    int id PK
    string protocol UK
    int client_id FK
    int professional_id FK
    int service_id FK
    datetime start_at
    datetime end_at
    string status
    string notes
    string source
    datetime created_at
    datetime updated_at
  }
  PROFESSIONALS ||--o{ AVAILABILITIES : possui
  PROFESSIONALS ||--o{ PROFESSIONAL_SERVICES : executa
  SERVICES ||--o{ PROFESSIONAL_SERVICES : "é executado"
  CLIENTS ||--o{ APPOINTMENTS : realiza
  PROFESSIONALS ||--o{ APPOINTMENTS : atende
  SERVICES ||--o{ APPOINTMENTS : refere
```
