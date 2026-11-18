# Falhas conhecidas e pendências

Estado em 2026-11-17. O código está publicado em `main` (https://github.com/LK-Projetos/AgendaPro); para o commit atual use `git log`. Pytest: 28 aprovados, 98% de cobertura. Playwright: 16 aprovados.

## Pendências de entrega (não feitas)
| ID | Item | Observação |
|---|---|---|
| P01 | 5 avaliações com pessoas reais e laudos preenchidos | Templates em `docs/laudos/`; **0 de 5 recebidas**; não foram simuladas |
| P02 | Homologação pessoal do vídeo | O vídeo original (5:00) não mostrava conflito, remarcação nem cancelamento, tinha ~88 s finais de tela parada, áudio baixo e dados expostos. A **versão revisada de 300,000 s foi produzida em 2026-11-17** (arquivo local, não versionado), com as demonstrações reais, imagens de GitHub, testes e modelagem, áudio normalizado e privacidade tratada. **Aguarda a homologação do autor** (assistir inteiro, conferir emendas e falas incorretas como "Flash API"). Ver [video/RELATORIO-CORTES.md](video/RELATORIO-CORTES.md), [video/PLANO-REVISAO-VIDEO.md](video/PLANO-REVISAO-VIDEO.md) e [video/HANDOFF-OUTRO-COMPUTADOR.md](video/HANDOFF-OUTRO-COMPUTADOR.md) |
| P03 | Testes unitários de componentes React | Não implementados (E2E com Playwright já existe: 16 cenários) |
| P04 | Capturas manuais complementares (opcional) | As 10 capturas automáticas existem em `docs/evidencias/capturas/`; para capturas manuais, abrir a aplicação e usar a ferramenta de recorte do sistema |
| P05 | Enviar commits de documentação ao GitHub | **Concluído** com o lote documental de 2026-11-17 (saneamento final e correção do DER); ver `git log` |
| P06 | Nomes dos integrantes/professor no README e vídeo | A informar |
| P07 | Submissão no AVA | Pendente; formato, tamanho e campos exigidos não foram confirmados ([10-checklist-submissao.md](10-checklist-submissao.md)) |

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
| F03 | O DER de `02-modelo-dados.md` não renderizava no GitHub ("Parse error on line 4 ... got ';'"): o Mermaid exige um atributo por linha, e os atributos estavam separados por `;` na mesma linha | Reescrito um atributo por linha (2026-11-17); validado com Mermaid 11.17.2 e 10.9.3 e conferido contra `models.py`; ver [11-auditoria-academica.md](11-auditoria-academica.md) |

Falhas relatadas por avaliadores humanos serão registradas aqui quando os laudos existirem.

## Achados da homologação (2026-11-16)
H01 (verificação de moeda), H02 (campo de preço com separador de milhar) e H03 (exclusões com diálogo real) — ver [04-testes.md](04-testes.md). H02 foi corrigido no código; H01 e H03 eram falhas da verificação manual, resolvidas pelo E2E.

## Reexecução de integridade (2026-11-17)
Em outro computador (Python 3.13.13, Node 24, Chrome): Pytest 28 aprovados, cobertura de linhas 98% (576 linhas, 9 não cobertas); Playwright 16 aprovados; typecheck e build do front-end OK. Os arquivos de `docs/evidencias/` continuam sendo os das execuções de 2026-11-16.
