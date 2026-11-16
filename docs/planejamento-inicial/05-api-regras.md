# API REST e regras de negócio

Base: `/api/v1`. JSON. Auth: `Authorization: Bearer <jwt>` nas rotas marcadas 🔒. Erro padrão: `{"code": "...", "message": "...", "details": {}}`.

## 1. Endpoints

### Autenticação (RF01)
| Método | Rota | Descrição | Sucesso | Erros |
|--------|------|-----------|---------|-------|
| POST | /auth/login | `{email, password}` → `{access_token, token_type, expires_in}` | 200 | 401 |
| GET | /auth/me 🔒 | Usuário atual | 200 | 401 |

### Dashboard (RF02)
| GET | /dashboard/summary 🔒 | `{today_count, next7_count, by_status, cancellation_rate, top_service}` | 200 |

### Clientes (RF03)
| Método | Rota | Descrição | Sucesso | Erros |
|--------|------|-----------|---------|-------|
| GET | /clients 🔒 | `?q=&page=&page_size=` | 200 | |
| POST | /clients 🔒 | Cria | 201 | 409 e-mail duplicado, 422 |
| GET | /clients/{id} 🔒 | Detalhe | 200 | 404 |
| PUT | /clients/{id} 🔒 | Atualiza | 200 | 404, 409, 422 |
| DELETE | /clients/{id} 🔒 | Exclui | 204 | 404, 409 com agendamentos futuros ativos |

### Serviços (RF04)
| GET | /services 🔒 | `?active=` | 200 |
| POST | /services 🔒 | Cria | 201 (422, 409 nome duplicado) |
| GET/PUT | /services/{id} 🔒 | Detalhe/atualiza | 200 (404, 422) |
| DELETE | /services/{id} 🔒 | Com histórico → desativa (soft); sem histórico → remove | 204 (404) |

### Profissionais e disponibilidade (RF05, RF06)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET/POST | /professionals 🔒 | Lista/cria |
| GET/PUT/DELETE | /professionals/{id} 🔒 | Detalhe/atualiza/desativa |
| PUT | /professionals/{id}/services 🔒 | `{service_ids: []}` substitui vínculos |
| GET | /professionals/{id}/availability 🔒 | Faixas semanais |
| PUT | /professionals/{id}/availability 🔒 | `[{weekday,start_time,end_time}]` substitui; 422 se sobrepor |

### Agendamentos (RF07, RF09)
| Método | Rota | Descrição | Sucesso | Erros |
|--------|------|-----------|---------|-------|
| GET | /appointments 🔒 | `?from=&to=&status=&professional_id=&client_id=` | 200 | |
| POST | /appointments 🔒 | `{client_id, service_id, professional_id, start_at, notes?}` → PENDING | 201 | 409 `SCHEDULE_CONFLICT`, 422 |
| GET | /appointments/{id} 🔒 | Detalhe | 200 | 404 |
| POST | /appointments/{id}/confirm 🔒 | PENDING → CONFIRMED | 200 | 409 `INVALID_TRANSITION` |
| POST | /appointments/{id}/reschedule 🔒 | `{start_at, professional_id?}` | 200 | 409 conflito/transição, 422 |
| POST | /appointments/{id}/cancel 🔒 | `{reason?}` | 200 | 409 |
| POST | /appointments/{id}/complete 🔒 | CONFIRMED → COMPLETED | 200 | 409 |

### Público (RF08) — sem autenticação
| Método | Rota | Descrição | Sucesso | Erros |
|--------|------|-----------|---------|-------|
| GET | /public/services | Serviços ativos | 200 | |
| GET | /public/services/{id}/professionals | Profissionais ativos que executam o serviço | 200 | 404 |
| GET | /public/slots | `?service_id=&professional_id=&date=YYYY-MM-DD` → horários livres | 200 | 422 |
| POST | /public/appointments | `{service_id, professional_id, start_at, client:{name,email,phone}}` → `{protocol, ...}` | 201 | 409, 422 |
| GET | /public/appointments/{protocol} | Consulta resumida (sem dados pessoais do cliente) | 200 | 404 |

Observação: cancelamento/remarcação pelo cliente final **não** está no MVP (ver pendências).

## 2. Regras de negócio
| ID | Regra |
|----|-------|
| RN01 | **Conflito**: dois agendamentos do mesmo profissional conflitam se `a.start < b.end` e `b.start < a.end` (intervalos semiabertos) e ambos têm status PENDING/CONFIRMED. CANCELLED/COMPLETED não bloqueiam. Retorna 409 `SCHEDULE_CONFLICT`. |
| RN02 | O intervalo inteiro `[start, end)` deve caber em uma faixa de disponibilidade do profissional naquele dia da semana (fuso America/Sao_Paulo). |
| RN03 | O profissional deve estar vinculado ao serviço e ambos ativos. |
| RN04 | `end_at = start_at + duration_minutes` do serviço, congelado na criação. |
| RN05 | `start_at` deve ser futuro com antecedência mínima configurável (padrão 60 min) para reservas públicas; o admin pode agendar com antecedência menor, mas não no passado. |
| RN06 | Início em múltiplos de 15 minutos. |
| RN07 | Confirmar: apenas PENDING. Concluir: apenas CONFIRMED. Cancelar: PENDING ou CONFIRMED. Remarcar: PENDING ou CONFIRMED. COMPLETED e CANCELLED são terminais. |
| RN08 | Remarcar revalida RN01–RN06 **excluindo o próprio agendamento**; em falha nada é alterado (transação). |
| RN09 | Reserva pública: cliente identificado por e-mail; se existir, reutiliza e não sobrescreve nome/telefone; senão cria. |
| RN10 | Serviço/profissional com agendamentos não pode ser excluído fisicamente: é desativado. Cliente com agendamentos ativos futuros não pode ser excluído (409). |
| RN11 | Reserva pública sempre nasce PENDING com `source=PUBLIC`; criada pelo admin nasce PENDING com `source=ADMIN`. |
| RN12 | Cálculo de horários livres: percorre faixas do dia em passos de 15 min, remove os que violam RN01/RN02/RN05. |
| RN13 | Disponibilidade: sem faixas sobrepostas por profissional/dia; `end_time > start_time`. |
| RN14 | Criação/remarcação executadas em transação com bloqueio de escrita (SQLite `BEGIN IMMEDIATE`) para evitar condição de corrida. |
| RN15 | Logs e respostas nunca contêm hash de senha, token ou dados de outros clientes. |
