# Divisão de execução entre dois agentes

Objetivo: trabalho paralelo sem conflito de arquivos. Cada agente é dono exclusivo de seus diretórios. O contrato entre eles é `docs/05-api-regras.md` (e o OpenAPI gerado pelo FastAPI).

## Agente A — Back-end e dados
**Dono exclusivo de:** `backend/**`, `.env.example` do back (`backend/.env.example`).
| Etapa | Entregas |
|-------|----------|
| A1 | Esqueleto FastAPI, config, sessão SQLAlchemy, Alembic, modelos, migração inicial |
| A2 | Segurança (hash, JWT), `/auth`, seed fictício |
| A3 | CRUD clientes, serviços, profissionais, vínculos, disponibilidade |
| A4 | AppointmentService (RN01–RN08, RN14), SlotService, endpoints de agendamento |
| A5 | Endpoints públicos e dashboard |
| A6 | Testes Pytest unitários e de integração (U01–U14, I01–I15) |
Saída para o Agente B: OpenAPI estável (`backend/openapi.json` exportado) ao fim de A1+A2 e a cada mudança de contrato.

## Agente B — Front-end e E2E
**Dono exclusivo de:** `frontend/**` (inclui `frontend/e2e/**`).
| Etapa | Entregas |
|-------|----------|
| B1 | Vite + React + TS, rotas, layout responsivo, cliente HTTP tipado (a partir do OpenAPI), mocks locais (MSW) enquanto o back não existe |
| B2 | Login, proteção de rotas, shell administrativo |
| B3 | Telas de clientes, serviços, profissionais, disponibilidade |
| B4 | Agenda/lista de agendamentos e ações (criar, confirmar, remarcar, cancelar) |
| B5 | Página pública de reserva e dashboard |
| B6 | Testes Playwright E01–E10 (contra back real, após A5) |

## Arquivos compartilhados (responsável único)
| Arquivo | Responsável | Regra |
|---------|-------------|-------|
| `docs/**` | Coordenação (arquiteto/humano) | Agentes só propõem alterações de contrato por mensagem |
| `README.md`, `.gitignore` | Coordenação | |
| `.github/workflows/ci.yml` | Coordenação, etapa final | Não executar sem autorização |
| `docs/13-registro-falhas.md` | Coordenação | Agentes enviam entradas; um único escritor |

## Protocolo
1. Mudança de contrato de API: Agente A abre proposta, coordenação atualiza `docs/05-api-regras.md`, só então B consome.
2. Branches: `feat/backend-*` (A) e `feat/frontend-*` (B); sem push, merge ou PR sem autorização do usuário.
3. Commits pequenos e em português, escopo no prefixo (`backend:`, `frontend:`, `docs:`).
4. Pontos de sincronização: S1 após A2/B2 (login ponta a ponta); S2 após A4/B4 (agendamento ponta a ponta); S3 após A6/B6 (testes completos).
5. Nenhum agente roda CI; testes apenas locais e sob demanda.
