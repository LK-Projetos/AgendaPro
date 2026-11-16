# Matriz de rastreabilidade

Cobertura **planejada**. A coluna de status será atualizada somente com execução real.

| Requisito | Critério de aceite | Regras | Endpoints | Tabelas | Testes | Backlog | Status |
|-----------|--------------------|--------|-----------|---------|--------|---------|--------|
| RF01 Autenticação | CA01 | RNF01, RNF02 | /auth/login, /auth/me | users | U12, I01, I02, E01 | T06, T07 | Planejado |
| RF02 Dashboard | CA12 | — | /dashboard/summary | appointments | U13, I14, E10 | T23 | Planejado |
| RF03 Clientes | CA02 | RN10 | /clients* | clients | I03, I04, E02 | T08, T09 | Planejado |
| RF04 Serviços | CA03 | RN10 | /services* | services | I05, E03 | T10, T11 | Planejado |
| RF05 Profissionais | CA04 | RN03 | /professionals*, /professionals/{id}/services | professionals, professional_services | U06, I06, E03 | T12, T13 | Planejado |
| RF06 Disponibilidade | CA05 | RN02, RN13 | /professionals/{id}/availability | availabilities | U04, U05, I06, E03 | T14, T15 | Planejado |
| RF07 Agendamentos | CA06–CA09 | RN04–RN08, RN11 | /appointments* | appointments | U07–U10, I07–I10, E04–E06 | T17–T20 | Planejado |
| RF08 Reserva pública | CA10, CA11 | RN05, RN09, RN12 | /public/* | appointments, clients | U11, U14, I11–I13, E07, E08 | T21, T22 | Planejado |
| RF09 Conflitos | CA06, CA11 | RN01, RN14 | /appointments, /public/appointments | appointments | U01–U03, I08, I13, E05 | T17, T21 | Planejado |
| RF10 Responsivo | CA13 | RNF09 | — | — | E09 | T04, T24 | Planejado |

## Rastreabilidade acadêmica
| Critério | Peso | Evidência prevista | Onde |
|----------|------|--------------------|------|
| Codificação | 20% | Repositório, histórico de commits | `backend/`, `frontend/` |
| Vídeo explicativo | 30% | Vídeo ~5 min | roteiro: `docs/08-roteiro-video.md` |
| Teste da solução | 25% | Saídas reais de Pytest/Playwright, cobertura | `docs/evidencias/` |
| Laudo de qualidade | 25% | 5 laudos de avaliadores reais | `docs/07-laudos/` |
| Documentação em Git | — | `docs/` versionado | este diretório |
| Modelo de dados | — | ER + dicionário | `docs/03`, `docs/04` |
| Registro de falhas | — | Falhas reais e correções | `docs/13-registro-falhas.md` (a criar) |
