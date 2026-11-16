# Backlog estruturado

Prioridade: **P0** indispensável ao MVP · **P1** importante · **P2** desejável (cortar primeiro). Estimativa em pontos relativos (1, 2, 3, 5, 8). Agente: A = back-end, B = front-end, C = coordenação.

## Fase 0 — Fundação
| ID | Item | Pri | Pts | Ag. | Depende |
|----|------|-----|-----|-----|---------|
| T01 | Aprovar planejamento e pendências P01–P11 | P0 | 1 | C | — |
| T02 | README, .gitignore, estrutura de pastas | P0 | 1 | C | T01 |
| T03 | Esqueleto FastAPI + config + sessão + Alembic | P0 | 3 | A | T02 |
| T04 | Esqueleto Vite/React/TS + rotas + layout responsivo base | P0 | 3 | B | T02 |

## Fase 1 — Autenticação e cadastros
| ID | Item | Pri | Pts | Ag. | Depende |
|----|------|-----|-----|-----|---------|
| T05 | Modelos + migração inicial + seed fictício | P0 | 3 | A | T03 |
| T06 | Segurança + `/auth` + testes U12, I01, I02 | P0 | 3 | A | T05 |
| T07 | Login e rotas protegidas no front | P0 | 3 | B | T04, T06 |
| T08 | CRUD clientes (API + testes) | P0 | 3 | A | T06 |
| T09 | CRUD clientes (UI) | P0 | 3 | B | T07, T08 |
| T10 | CRUD serviços (API + testes) | P0 | 3 | A | T06 |
| T11 | CRUD serviços (UI) | P0 | 3 | B | T07, T10 |
| T12 | Profissionais + vínculo com serviços (API + testes) | P0 | 3 | A | T10 |
| T13 | Profissionais (UI) | P0 | 3 | B | T11, T12 |
| T14 | Disponibilidade semanal (API + RN13) | P0 | 3 | A | T12 |
| T15 | Disponibilidade (UI) | P0 | 3 | B | T13, T14 |

## Fase 2 — Núcleo de agendamento
| ID | Item | Pri | Pts | Ag. | Depende |
|----|------|-----|-----|-----|---------|
| T16 | SlotService (RN12) + testes U11 | P0 | 5 | A | T14 |
| T17 | AppointmentService: criar + conflito + disponibilidade (RN01–RN06, RN14) | P0 | 8 | A | T16 |
| T18 | Confirmar, concluir, cancelar, remarcar (RN07, RN08) | P0 | 5 | A | T17 |
| T19 | Testes U01–U10, I07–I10 | P0 | 5 | A | T18 |
| T20 | UI de agendamentos (lista/agenda, criar, ações, erros de conflito) | P0 | 8 | B | T18 |

## Fase 3 — Público e indicadores
| ID | Item | Pri | Pts | Ag. | Depende |
|----|------|-----|-----|-----|---------|
| T21 | Endpoints `/public/*` + RN09 + teste de corrida I13 | P0 | 5 | A | T18 |
| T22 | Página pública de reserva (fluxo em passos, mobile first) | P0 | 5 | B | T21 |
| T23 | Dashboard (API + UI) | P1 | 5 | A+B | T18 |
| T24 | Revisão de responsividade e acessibilidade | P1 | 3 | B | T22 |
| T25 | Busca/paginação em clientes e agendamentos | P1 | 2 | A+B | T09, T20 |

## Fase 4 — Qualidade e entrega
| ID | Item | Pri | Pts | Ag. | Depende |
|----|------|-----|-----|-----|---------|
| T26 | Testes de integração restantes (I03–I15) | P0 | 5 | A | T21 |
| T27 | Testes Playwright E01–E10 | P0 | 8 | B | T22, T23 |
| T28 | Medição real de cobertura e execução local completa | P0 | 2 | A+B | T26, T27 |
| T29 | Recrutar e conduzir 5 avaliações reais; coletar laudos | P0 | 5 | C | T24 |
| T30 | Registro de falhas e correções; reteste | P0 | 5 | A+B | T29 |
| T31 | Escrever `ci.yml` (sem executar) | P1 | 2 | C | T28 |
| T32 | Gravar e editar vídeo (~5 min) | P0 | 5 | C | T30 |
| T33 | Relatório final, matriz de rastreabilidade atualizada, tag de entrega | P0 | 2 | C | T32 |
| T34 | Execução final de CI e push/merge — **só com autorização** | P1 | 1 | C | T33 |

## Pós-MVP (fora de escopo atual)
Cancelamento pelo cliente via protocolo (P01), bloqueios pontuais (P02), notificações, pagamentos, IA, integrações.

## Definição de pronto (DoD)
Código revisado; testes do item passando localmente; docs atualizadas; commit; critérios de aceite do PRD verificados.
