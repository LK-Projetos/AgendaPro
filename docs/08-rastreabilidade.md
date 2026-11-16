# Matriz de rastreabilidade

Cada requisito ([01-requisitos.md](01-requisitos.md)) → implementação → testes que o exercitam (Pytest em `backend/tests/`, E2E em `frontend/e2e/agendapro.spec.ts`).

| Requisito | Implementação | Pytest | E2E |
|---|---|---|---|
| RF01 Dashboard | `services.DashboardService`, `GET /api/dashboard`, `pages/Dashboard.tsx` | `test_dashboard` | 01, 15 |
| RF02 CRUD clientes | `ClientService`, `/api/clients`, `pages/Clients.tsx` | `test_client_crud`, `_duplicate_email`, `_update_same_email…`, `_not_found`, `_with_appointments_cannot_be_deleted` | 03–06, 14 |
| RF03 CRUD serviços | `ServiceService`, `/api/services`, `pages/Services.tsx` | `test_service_crud`, `_validation`, `_duplicate_name…`, `_with_appointments_cannot_be_deleted` | 07–09, 14 |
| RF04 CRUD agendamentos | `AppointmentService`, `/api/appointments`, `pages/Appointments.tsx` | `test_create_computes_end_and_lists`, `test_update_*`, `test_delete`, `test_filters` | 02, 10 |
| RF05 Remarcar/cancelar | `reschedule()`, `cancel()` | `test_reschedule_*`, `test_cancel_twice_conflict_and_404` | 12, 13 |
| RF06 Conflito de horário | `_validate_slot` + `find_conflict` (RN01) | `test_conflict_overlaps_rejected`, `test_adjacent_is_allowed`, `test_cancelled_does_not_block` | 11, 12, 13 |
| RF07 Validação de formulários | `schemas.py` + `validate()` nas páginas | `test_client_validation`, `test_service_validation`, `test_validation_and_references`, `test_past_rejected` | 03, 05, 08 |
| RF08 Persistência SQLite | `database.py`, `models.py` | `test_data_survives_engine_restart`, `test_foreign_keys_enforced` | 15 + [persistencia-reinicio.txt](evidencias/persistencia-reinicio.txt) |
| RF09 Tratamento de erros | `errors.py`, `ApiError` em `api.ts`, toasts e alertas | `test_client_not_found`, `test_cancel_twice…`, 409/422 em vários | 05, 11, 14 |
| RF10 Dados fictícios | `seed.py` | `test_seed_creates_fake_data_and_is_idempotent` | 01, 02 |
| RNF02 Responsivo | `index.css` (breakpoint 680 px) | — | 16 |

## Critérios acadêmicos
| Critério | Peso | Evidência existente | Pendente |
|---|---|---|---|
| Codificação | 20% | `backend/`, `frontend/`, histórico Git | Push ao GitHub (sem permissão até agora) |
| Vídeo explicativo | 30% | Roteiro [06-roteiro-video.md](06-roteiro-video.md) | **Gravar o vídeo** |
| Teste da solução | 25% | Pytest, E2E, build, persistência, capturas | — |
| Laudo de qualidade | 25% | Templates [laudos/](laudos/) | **5 avaliações humanas reais** |
