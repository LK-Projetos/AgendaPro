# API REST

Base: `http://127.0.0.1:8000/api` · JSON · documentação interativa em `/docs` (OpenAPI) · sem autenticação (demonstração).

## Endpoints
| Método | Rota | Descrição | Sucesso | Erros |
|---|---|---|---|---|
| GET | /health | Verifica a API | 200 | |
| GET | /dashboard | Indicadores | 200 | |
| GET | /clients?q= | Lista/busca clientes | 200 | |
| POST | /clients | Cria | 201 | 409 e-mail duplicado, 422 |
| GET | /clients/{id} | Detalhe | 200 | 404 |
| PUT | /clients/{id} | Atualiza | 200 | 404, 409, 422 |
| DELETE | /clients/{id} | Exclui | 204 | 404, 409 se tem agendamentos |
| GET/POST | /services | Lista / cria | 200 / 201 | 409 nome duplicado, 422 |
| GET/PUT/DELETE | /services/{id} | Detalhe / atualiza / exclui | 200 / 200 / 204 | 404, 409, 422 |
| GET | /appointments?status=&date_from=&date_to=&client_id= | Lista (ordenada por início) | 200 | 422 filtro inválido |
| POST | /appointments | Cria `{client_id, service_id, start_at, notes?}` | 201 | 409 `SCHEDULE_CONFLICT`, 422 |
| GET | /appointments/{id} | Detalhe | 200 | 404 |
| PUT | /appointments/{id} | Edita (revalida conflito) | 200 | 404, 409, 422 |
| POST | /appointments/{id}/reschedule | `{start_at}` mantém a duração | 200 | 404, 409, 422 |
| POST | /appointments/{id}/cancel | Cancela | 200 | 404, 409 |
| DELETE | /appointments/{id} | Exclui o registro | 204 | 404 |

`start_at` em ISO 8601 local, ex.: `2030-01-08T10:00`.

## Formato de erro
```json
{ "code": "SCHEDULE_CONFLICT", "message": "Horário indisponível: já existe um agendamento neste intervalo.",
  "details": { "conflict_id": 4, "conflict_start": "2026-11-16T18:00:00", "conflict_end": "2026-11-16T18:30:00" } }
```
Códigos: `VALIDATION_ERROR` (422, `details.fields` por campo), `BUSINESS_RULE` (422), `NOT_FOUND` (404), `CONFLICT` (409), `SCHEDULE_CONFLICT` (409), `DATABASE_ERROR` (500).

## Exemplo de resposta de agendamento
```json
{ "id": 11, "client": {"id": 1, "name": "Ana Exemplo"},
  "service": {"id": 1, "name": "Corte de cabelo", "duration_minutes": 30, "price": 50.0},
  "start_at": "2026-11-16T20:00:00", "end_at": "2026-11-16T20:30:00", "status": "SCHEDULED", "notes": null }
```
