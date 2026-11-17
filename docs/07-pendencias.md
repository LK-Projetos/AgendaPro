# Falhas conhecidas e pendências

## Pendências de entrega (não feitas)
| ID | Item | Observação |
|---|---|---|
| P01 | 5 avaliações com pessoas reais e laudos preenchidos | Templates em `docs/laudos/`; não foram simulados |
| P02 | Vídeo (~5 min) | **Original gravado (5:00), mas incompleto:** não mostra conflito, remarcação nem cancelamento e tem ~88 s finais de tela parada. **Versão revisada ainda não produzida.** Faltam 4 clipes complementares. Ver [video/PLANO-REVISAO-VIDEO.md](video/PLANO-REVISAO-VIDEO.md), [video/ROTEIRO-CAPTURA.md](video/ROTEIRO-CAPTURA.md) e [video/HANDOFF-OUTRO-COMPUTADOR.md](video/HANDOFF-OUTRO-COMPUTADOR.md) |
| P03 | Testes unitários de componentes React | Não implementados (E2E com Playwright já existe: 16 cenários) |
| P04 | Capturas manuais complementares (opcional) | As 10 capturas automáticas existem em `docs/evidencias/capturas/`; para capturas manuais, abrir a aplicação e usar a ferramenta de recorte do sistema |
| P05 | Enviar commits de documentação ao GitHub | Concluído até `3e33ff6`; a preparação dos laudos e o handoff do vídeo são publicados em 2026-11-17 (ver `git log`) |
| P06 | Nomes dos integrantes/professor no README e vídeo | A informar |

## Limitações técnicas conhecidas
| ID | Limitação | Impacto |
|---|---|---|
| L01 | Verificação de conflito e gravação não estão sob bloqueio explícito (SQLite serializa escritas, mas duas requisições simultâneas ao mesmo horário não foram testadas) | Risco teórico de duplo agendamento sob concorrência; irrelevante em demonstração de usuário único |
| L02 | Sem autenticação (conforme escopo) | API aberta; usar só localmente com dados fictícios |
| L03 | Horários sem fuso; sem horário de funcionamento nem folgas | Permite agendar de madrugada |
| L04 | Sem paginação nas listas | Adequado ao volume do MVP |
| L05 | Aviso de lint (fast refresh) em `components.tsx`; aviso de depreciação do `httpx`/Starlette no Pytest | Sem impacto funcional |
| L06 | Preço em `FLOAT` | Suficiente para o MVP; o ideal seria inteiro em centavos/decimal |
| L07 | Dashboard e seed usam a data do sistema; o seed é relativo à data em que for executado | Valores do dashboard variam por dia |
| L08 | Aba atual lida do `#hash` só ao carregar a página | Mudar o hash manualmente não troca a aba sem recarregar |

## Falhas encontradas e corrigidas durante o desenvolvimento
| ID | Falha | Correção |
|---|---|---|
| F01 | `TypeError` ao importar `repositories.py`: o método `list` da classe sombreava o tipo `list[...]` nas anotações | `from __future__ import annotations` (detectado ao rodar o Pytest pela primeira vez) |
| F02 | Validador de `start_at` reutilizado por `RescheduleIn` chamava um método decorado | Extraída função `normalize_start` |

Falhas relatadas por avaliadores humanos serão registradas aqui quando os laudos existirem.

## Achados da homologação (2026-11-16)
H01 (verificação de moeda), H02 (campo de preço com separador de milhar) e H03 (exclusões com diálogo real) — ver [04-testes.md](04-testes.md). H02 foi corrigido no código; H01 e H03 eram falhas da verificação manual, resolvidas pelo E2E.
