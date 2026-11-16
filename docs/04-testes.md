# Testes

Todos os resultados abaixo vêm de execuções reais em 2026-11-16 (Windows 11, Python 3.13.15, Node 24). Saídas completas em [evidencias/](evidencias/).

## 1. Testes automatizados do back-end (Pytest)
Comando: `cd backend && python -m pytest -v --cov=app --cov-report=term-missing`
**Resultado: 28 passed, 0 failed. Cobertura de linhas de `app/`: 98%** ([pytest-saida.txt](evidencias/pytest-saida.txt)). O relógio é congelado nos testes (2030-01-07 08:00) para torná-los determinísticos. Os testes usam SQLite em memória; os de persistência usam arquivo temporário.

| Arquivo | O que verifica |
|---|---|
| `tests/test_clients_services.py` | CRUD de clientes e serviços, normalização (e-mail, telefone, preço), validações (422 com campos), e-mail/nome duplicado (409), 404, bloqueio de exclusão com agendamentos |
| `tests/test_appointments.py` | Criação com fim calculado; **conflitos** (sobreposição parcial/total/início anterior) → 409; adjacência permitida; cancelado não bloqueia; passado rejeitado; múltiplos de 15 min; referências inexistentes; remarcar OK e remarcar em conflito mantendo o original; remarcar cancelado/passado; cancelar duas vezes; editar com revalidação; excluir; filtros; dashboard com valores calculados à mão |
| `tests/test_persistence_seed.py` | Dados sobrevivem a reinício do engine (arquivo SQLite); chaves estrangeiras impostas; seed cria 6 clientes, 4 serviços, 10 agendamentos fictícios e é idempotente |

## 2. Verificação estática do front-end
`npm run typecheck`: sem erros. `npm run lint` (oxlint): 1 aviso (fast refresh em `components.tsx`, sem impacto). `npm run build`: sucesso ([frontend-build.txt](evidencias/frontend-build.txt)).

## 3. Validação manual da aplicação em navegador
Executada por mim (Claude) no navegador embutido, contra a API real e o banco SQLite com seed, via interface (cliques e preenchimento de formulários, parte via script no console do navegador). **Não é avaliação humana** e não substitui os laudos. Registro: [validacao-navegador.md](evidencias/validacao-navegador.md).

## 4. Não realizado / limitações
- **Sem testes E2E automatizados** (Playwright não configurado nesta entrega) e **sem testes automatizados do front-end** (componentes).
- Sem capturas de tela salvas (a captura do navegador excedeu o tempo na tentativa).
- Sem teste de concorrência (duas requisições simultâneas ao mesmo horário); o SQLite serializa escritas, mas a verificação de conflito e a gravação não estão sob bloqueio explícito (ver pendências).
- Testado em um único navegador/ambiente.
- Os 5 laudos de avaliadores humanos **não foram feitos**; templates em [laudos/](laudos/).
- CI não configurada (conforme regra do projeto).
