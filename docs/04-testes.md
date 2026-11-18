# Relatório técnico de testes

Todos os resultados vêm de execuções reais em 2026-11-16 (Windows 11, Python 3.13.15, Node 24, Google Chrome). Saídas completas em [evidencias/](evidencias/). Nenhum resultado foi simulado.

## Resumo
| Nível | Ferramenta | Resultado | Evidência |
|---|---|---|---|
| API (unitário/integração) | Pytest | **28 passed, 0 failed**; cobertura de linhas de `app/`: **98%** (576 linhas, 9 não cobertas) | [pytest-saida.txt](evidencias/pytest-saida.txt) |
| Front-end estático | tsc / oxlint / Vite build | typecheck e build OK; lint com 1 aviso (fast refresh) | [frontend-build.txt](evidencias/frontend-build.txt) |
| E2E (navegador real) | Playwright + Chrome | **16 passed, 0 failed** (duas execuções consecutivas, a segunda salva) | [e2e-saida.txt](evidencias/e2e-saida.txt) |
| Persistência após reinício | script com processo uvicorn real | dados mantidos após parar e iniciar a API | [persistencia-reinicio.txt](evidencias/persistencia-reinicio.txt) |
| Capturas de tela | Playwright | 10 imagens | [capturas/](evidencias/capturas/) |

Reexecução de integridade em 2026-11-17 (outro computador; Python 3.13.13, Node 24, Chrome): Pytest 28 passed, 98%; Playwright 16 passed; typecheck e build OK. As saídas arquivadas em `evidencias/` continuam sendo as de 2026-11-16.

## 1. Pytest (API) — como executar
`cd backend && python -m pytest -v --cov=app --cov-report=term-missing`
Relógio congelado (2030-01-07 08:00) para determinismo; SQLite em memória (persistência usa arquivo temporário).

| Arquivo | Verifica |
|---|---|
| `tests/test_clients_services.py` | CRUD de clientes e serviços, normalização, validações 422, duplicidade 409, 404, bloqueio de exclusão com agendamentos |
| `tests/test_appointments.py` | Fim calculado; conflitos (parcial/total/início anterior) → 409; adjacência permitida; cancelado não bloqueia; passado; múltiplos de 15; referências; remarcar OK/conflito mantendo original; cancelar duas vezes; editar; excluir; filtros; dashboard |
| `tests/test_persistence_seed.py` | Persistência entre engines, chaves estrangeiras, seed fictício idempotente |

## 2. E2E (Playwright) — como executar
`cd frontend && npm run e2e` (usa o Google Chrome instalado; não baixa navegadores).
Ambiente **isolado e sem mocks**: a configuração sobe a API real na porta 8001 com um banco SQLite descartável (`frontend/e2e/.tmp/e2e.db`, recriado a cada execução e populado pelo seed fictício) e o front na 5174. O banco de demonstração `backend/agendapro.db` não é tocado. Diálogos de confirmação são os do navegador (aceitos/recusados pelo teste).

| # | Cenário | Cobre |
|---|---|---|
| 01 | Dashboard carrega indicadores do banco (clientes 6, serviços 4, cancelados 2) | Dashboard |
| 02 | Abas Agendamentos, Clientes e Serviços abrem com dados do seed (10 agendamentos) | Telas |
| 03 | Formulário de cliente vazio mostra 3 erros | Validação |
| 04 | Cadastro de cliente | Cliente |
| 05 | E-mail duplicado rejeitado | Validação/regra |
| 06 | Edição de cliente | Cliente |
| 07 | Cadastro de serviço com preço `90,50` exibido como R$ 90,50 | Serviço/monetário |
| 08 | Duração inválida, preço `abc` e `-5` rejeitados | Validação/monetário |
| 09 | Edição de serviço com `1.234,56`; campo reabre como `90,50` | Serviço/monetário |
| 10 | Criação de agendamento com fim calculado (10:00 → 10:45) | Agendamento |
| 11 | Conflito (10:30) rejeitado, nada criado; horário encostado (10:45) permitido | Conflito |
| 12 | Remarcar em conflito mantém original; remarcar para 14:00 atualiza | Remarcação |
| 13 | Cancelar: recusar mantém; aceitar cancela; horário volta a ficar livre | Cancelamento |
| 14 | Exclusões com confirmação real; bloqueio de cliente/serviço com agendamentos; recusar/aceitar exclusão | Exclusões |
| 15 | Recarregar a página mantém dados; dashboard reflete (7 clientes, 5 serviços, 3 cancelados) | Persistência/dashboard |
| 16 | 375×812: sem rolagem horizontal nas 4 abas | Responsivo |

## 3. Problemas encontrados nesta fase
| ID | Achado | Tratamento |
|---|---|---|
| H01 | Na validação manual anterior, a verificação de "criado/editado" de serviço deu falso por eu comparar `R$ 90,50` com espaço comum, enquanto o `Intl` usa espaço não separável | Corrigido o critério (regex `\s`); E2E 07 e 09 confirmam criação e edição de serviço |
| H02 | Campo de preço só aceitava `,` ou `.` simples; `1.234,56` falhava | Corrigido: `parsePrice` aceita `90`, `90.5`, `90,50`, `R$ 1.234,56`; rejeita texto e negativos; campo de edição exibe `90,50` |
| H03 | Exclusões foram validadas antes com `window.confirm` substituído por script | Refeito no E2E com diálogos reais do navegador (aceitar e recusar) |

## 4. Limitações (não verificado)
- Navegador único (Chrome); sem testes em Firefox/Safari ou em celular físico.
- Sem testes unitários de componentes React isolados.
- Sem teste de requisições simultâneas ao mesmo horário (limitação L01 em [07-pendencias.md](07-pendencias.md)).
- Sem teste de carga/desempenho.
- As capturas são do navegador desktop 1280×800 (e uma em 375×812); a captura do modal pega a página inteira, por isso o fundo escurecido cobre só a primeira tela.
- Nenhuma avaliação humana foi realizada; os laudos estão em branco.
- CI não configurada, conforme regra do projeto.
