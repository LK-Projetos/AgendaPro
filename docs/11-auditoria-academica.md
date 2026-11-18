# Auditoria acadêmica da documentação (2026-11-17)

Escopo: conferência de `01-requisitos` a `10-checklist-submissao` e dos documentos de vídeo e laudos contra o código (`backend/app/models.py`, `schemas.py`, `services.py`, `routers/api.py`, `frontend/src`). Nenhum código nem banco foi alterado. Esta auditoria **não declara a entrega concluída**.

## 1. Correção do DER
- **Causa:** em `02-modelo-dados.md` os atributos das entidades estavam em uma linha, separados por `;` (`CLIENTS { int id PK; string name; ... }`). A sintaxe `erDiagram` do Mermaid exige **um atributo por linha** entre `{` e `}`; o `;` gera `Parse error on line 4 ... got ';'`, mensagem que o GitHub exibia como "Unable to render rich display".
- **Correção:** atributos reescritos um por linha, com os mesmos nomes, tipos e chaves (PK/FK/UK), mais comentários curtos com as restrições reais (NN, CHECK). Relacionamentos e rótulos mantidos.
- **Validação:** o bloco antigo reproduz o erro em Mermaid 11.17.2 e 10.9.3; o bloco novo e o diagrama de classes são aceitos e renderizados pelas duas versões (Chrome headless). Conferência automática contra `Base.metadata` do SQLAlchemy: 3 tabelas, 19 colunas, tipos, PK, UK, FK e anulabilidade idênticos; FKs `appointments.client_id → clients` e `appointments.service_id → services`; cardinalidade `||--o{` coerente com FK `NOT NULL` (um cliente/serviço, zero ou mais agendamentos).
- A renderização no GitHub é conferida após o push (resultado no relatório da entrega).

## 2. Pontos aprovados (conferidos com o código)
- API (`03-api.md`) corresponde às rotas de `routers/api.py`, aos códigos de erro de `errors.py` e ao formato `{code,message,details}`.
- Regras RN01–RN10 (`01-requisitos.md`) correspondem a `services.py` e `schemas.py`: conflito `início_A < fim_B e fim_A > início_B` apenas entre `SCHEDULED`, passado → 422, múltiplos de 15, só `SCHEDULED` remarcável, exclusão bloqueada por agendamentos, normalização de e-mail/telefone.
- Dicionário de dados coerente com `models.py` (tipos, tamanhos, CHECKs, índice `ix_appointments_range`, `PRAGMA foreign_keys=ON`).
- Testes: Pytest reexecutado em 2026-11-17 neste ambiente, 28 passed, cobertura 98% (576 linhas, 9 não cobertas), como em `04-testes.md`; E2E reexecutado, 16 passed. Os arquivos em `docs/evidencias/` seguem sendo os das execuções de 2026-11-16 (tempos diferentes, mesmos resultados).

## 3. Contradições e itens desatualizados (corrigidos no lote final de 2026-11-17)
| Documento | Problema encontrado | Tratamento |
|---|---|---|
| `08-rastreabilidade.md` | Critérios diziam "sem permissão" para o push e "gravar o vídeo" | Atualizado: código publicado, vídeo revisado produzido (homologação pendente), laudos 0 de 5, submissão no AVA pendente |
| `09-relatorio-entrega.md` | Veredito dizia que faltava publicar no GitHub, em contradição com as seções 5 e 8; citava `7b76374` como estado atual | Veredito, pendências, estado do Git e prontidão reescritos; `7b76374` mantido apenas como evento histórico da publicação inicial |
| `07-pendencias.md`, `PLANO-REVISAO-VIDEO.md`, `ROTEIRO-CAPTURA.md`, laudos e `RELATORIO-CONSOLIDADO.md` | Citavam `3e33ff6` como estado atual do GitHub | Referências ao estado atual trocadas por "ver `git log`"; `3e33ff6` mantido onde descreve um evento passado, rotulado como tal |
| `07-pendencias.md`, `PLANO-REVISAO-VIDEO.md`, `HANDOFF-OUTRO-COMPUTADOR.md` | Diziam que o vídeo revisado não fora produzido | Atualizados (produzido, aguardando homologação); textos do plano original mantidos como histórico; "Próxima missão" do handoff reescrita |
| `02-modelo-dados.md` (diagrama de classes) | Omitia `get()`/`list()` e os métodos privados | Métodos conferidos contra `services.py` (`ClientService`, `ServiceService`, `AppointmentService`); nenhuma estrutura nova foi inventada |
| `05-manual-de-uso.md`, `06-roteiro-video.md` | Manual não citava passado/múltiplos de 15; roteiro apresentado como o vídeo final | Manual completado conforme RN03/RN04/RN06; roteiro marcado como planejamento original |
| `04-testes.md` | Só registrava as execuções de 2026-11-16 | Nota da reexecução de 2026-11-17 acrescentada |
| `01-requisitos.md` RN08 vs banco | Unicidade de nome de serviço sem diferenciar maiúsculas é checada em `ServiceRepository.get_by_name`; a constraint `UNIQUE` do SQLite diferencia maiúsculas | Mantido (sem impacto; regra garantida na camada de serviço) |
| `docs/planejamento-inicial/` | Descreve um escopo maior já superado | Mantido como histórico, não revisado |

## 4. Pendências reais da entrega (não resolvidas por esta auditoria)
1. **Vídeo:** produzido com 300,000 s (ver [video/RELATORIO-CORTES.md](video/RELATORIO-CORTES.md)), mas depende da homologação do autor (assistir inteiro; a transcrição automática não é confiável; falas incorretas no original: "Flash API", "Playwriter").
2. **Laudos de qualidade (25%):** 0 de 5 avaliações humanas reais recebidas; nenhuma nota ou opinião foi simulada.
3. Nomes da equipe e do professor no README e no vídeo.
4. Formatos e campos exigidos pelo AVA, não confirmados.
5. Submissão no AVA.
6. Limitações técnicas conhecidas L01–L08 (`07-pendencias.md`).
