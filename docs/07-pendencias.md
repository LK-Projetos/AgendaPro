# Falhas conhecidas e pendências

## Pendências de entrega (não feitas)
| ID | Item | Observação |
|---|---|---|
| P01 | 5 avaliações com pessoas reais e laudos preenchidos | Templates em `docs/laudos/`; não foram simulados |
| P02 | Gravação do vídeo (~5 min) | Roteiro em `docs/06-roteiro-video.md` |
| P03 | Testes E2E automatizados (Playwright) e testes de componentes do front | Não implementados |
| P04 | Capturas de tela como evidência | Não geradas |
| P05 | Push para o GitHub | Aguardando autorização; commit apenas local |
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
