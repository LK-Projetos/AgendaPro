# Dicionário de dados

Convenções: `PK` chave primária, `FK` chave estrangeira, `UK` única, `NN` não nulo. Datas/horas em UTC (ISO 8601), exceto `start_time`/`end_time` de disponibilidade (hora local do estabelecimento, America/Sao_Paulo).

## users
| Coluna | Tipo | Restrições | Descrição |
|--------|------|-----------|-----------|
| id | INTEGER | PK, autoinc | Identificador |
| email | VARCHAR(120) | UK, NN | Login do administrador |
| password_hash | VARCHAR(255) | NN | Hash bcrypt/argon2 |
| name | VARCHAR(100) | NN | Nome de exibição |
| active | BOOLEAN | NN, default true | Permite login |

## clients
| Coluna | Tipo | Restrições | Descrição |
|--------|------|-----------|-----------|
| id | INTEGER | PK | |
| name | VARCHAR(120) | NN, 2–120 chars | Nome completo |
| email | VARCHAR(120) | UK, NN, formato e-mail | Identifica o cliente na reserva pública |
| phone | VARCHAR(20) | NN, 10–15 dígitos | Telefone fictício nos testes |
| notes | TEXT | nulo | Observações internas |
| created_at | DATETIME | NN | Criação |

## services
| Coluna | Tipo | Restrições | Descrição |
|--------|------|-----------|-----------|
| id | INTEGER | PK | |
| name | VARCHAR(100) | UK, NN | Nome do serviço |
| description | TEXT | nulo | |
| duration_minutes | INTEGER | NN, 15–480, múltiplo de 15 | Duração |
| price | NUMERIC(10,2) | NN, ≥ 0 | Preço de referência (sem cobrança) |
| active | BOOLEAN | NN, default true | Visível na página pública |

## professionals
| Coluna | Tipo | Restrições | Descrição |
|--------|------|-----------|-----------|
| id | INTEGER | PK | |
| name | VARCHAR(120) | NN | |
| email | VARCHAR(120) | nulo | Contato |
| active | BOOLEAN | NN, default true | |

## professional_services (N:N)
| Coluna | Tipo | Restrições |
|--------|------|-----------|
| professional_id | INTEGER | PK, FK → professionals.id, ON DELETE CASCADE |
| service_id | INTEGER | PK, FK → services.id, ON DELETE CASCADE |

## availabilities
| Coluna | Tipo | Restrições | Descrição |
|--------|------|-----------|-----------|
| id | INTEGER | PK | |
| professional_id | INTEGER | FK, NN | |
| weekday | INTEGER | NN, 0–6 (0 = segunda) | Dia da semana |
| start_time | TIME | NN | Início da faixa |
| end_time | TIME | NN, > start_time | Fim da faixa |

Regra: não pode haver faixas sobrepostas para o mesmo `professional_id` + `weekday` (RN13).

## appointments
| Coluna | Tipo | Restrições | Descrição |
|--------|------|-----------|-----------|
| id | INTEGER | PK | |
| protocol | VARCHAR(12) | UK, NN | Código público (ex.: `AP-7K3Q9X`) |
| client_id | INTEGER | FK, NN | |
| professional_id | INTEGER | FK, NN | |
| service_id | INTEGER | FK, NN | |
| start_at | DATETIME | NN | Início (UTC) |
| end_at | DATETIME | NN, > start_at | start_at + duração do serviço no momento da criação |
| status | VARCHAR(12) | NN, CHECK in (PENDING, CONFIRMED, CANCELLED, COMPLETED) | |
| notes | TEXT | nulo | |
| source | VARCHAR(10) | NN, in (ADMIN, PUBLIC) | Origem |
| created_at / updated_at | DATETIME | NN | Auditoria |

Índices: `(professional_id, start_at, end_at)` para conflito; `(status)`; `(client_id)`; `(start_at)`.

## Dados de seed (fictícios)
1 admin (`admin@agendapro.test`), 3 serviços, 2 profissionais, disponibilidade seg–sex 09:00–18:00, 5 clientes fictícios, ~10 agendamentos em estados variados. Nenhum dado pessoal real.
