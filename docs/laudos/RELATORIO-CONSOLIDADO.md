# Relatório Consolidado de Avaliação — AgendaPro

**Disciplina:** Projeto Integrador Transdisciplinar em Engenharia de Software II — Cruzeiro do Sul Virtual
**Versão avaliada:** código em `b4252fb` (2026-11-16); documentação até `3e33ff6`
**Repositório:** https://github.com/LK-Projetos/AgendaPro
**Status do documento:** **PARCIAL.** As seções A e B estão concluídas com evidências reais. A seção C (avaliações humanas independentes) **não foi realizada**: 0 de 5 laudos recebidos.

## 1. Apresentação
O AgendaPro é um MVP web de agendamentos para um estabelecimento com um profissional. Stack: React 19 + TypeScript + Vite; Python 3.13 + FastAPI; SQLAlchemy 2 + SQLite. Funcionalidades implementadas: dashboard, CRUD de clientes e serviços, criação/edição/remarcação/cancelamento/exclusão de agendamentos, bloqueio de conflito, validação front e back, persistência e layout responsivo (`docs/01-requisitos.md`, `docs/08-rastreabilidade.md`).

## 2. Objetivo da avaliação
Verificar se o MVP cumpre os requisitos RF01–RF10 e as regras RN01–RN10, e coletar a percepção de cinco usuários reais sobre uso, clareza e confiabilidade.

## 3. Metodologia
| Parte | O que é | Quem executa | Situação |
|---|---|---|---|
| A | Testes automatizados (Pytest, Playwright, build) | Ferramentas, definidas pela equipe | Concluída |
| B | Testes de interface feitos pela equipe (capturas e validação em navegador) | Equipe | Concluída |
| C | Avaliações humanas independentes com os formulários `laudo-avaliador-1..5` | 5 avaliadores externos | **Pendente (0/5)** |

## 4. Resultados — A) Testes automatizados
Execuções reais de 2026-11-16 (Windows 11, Python 3.13, Node 24, Chrome). Detalhes em `docs/04-testes.md`.
| Teste | Resultado | Evidência |
|---|---|---|
| Pytest (API) | 28 aprovados, 0 falhas; cobertura de linhas 98% (576 linhas, 9 não cobertas) | `docs/evidencias/pytest-saida.txt` |
| E2E Playwright (Chrome, sem mocks) | 16 aprovados, 0 falhas, em duas execuções consecutivas | `docs/evidencias/e2e-saida.txt` |
| typecheck / build | OK; lint com 1 aviso (fast refresh) | `docs/evidencias/frontend-build.txt` |
| Persistência após reinício da API | Dados mantidos | `docs/evidencias/persistencia-reinicio.txt` |

Teste automatizado não equivale a avaliação humana e não é contabilizado na seção C.

## 5. Resultados — B) Testes de interface pela equipe
Validação manual em navegador e 10 capturas de tela (dashboard, abas, validações, agendamento criado, conflito rejeitado, cancelamento, mobile 375×812) em `docs/evidencias/capturas/` e `docs/evidencias/validacao-navegador.md`. Realizados pelos próprios desenvolvedores; **não são independentes**.

## 6. Resultados — C) Avaliações humanas independentes
| Avaliador | Laudo | Registro recebido | Data do teste | Status |
|---|---|---|---|---|
| 1 | `laudo-avaliador-1.md` / PDF | Nenhum | — | Pendente |
| 2 | `laudo-avaliador-2.md` / PDF | Nenhum | — | Pendente |
| 3 | `laudo-avaliador-3.md` / PDF | Nenhum | — | Pendente |
| 4 | `laudo-avaliador-4.md` / PDF | Nenhum | — | Pendente |
| 5 | `laudo-avaliador-5.md` / PDF | Nenhum | — | Pendente |

Busca realizada em 2026-11-17 no repositório (incluindo `docs/evidencias/avaliador-N/`) e na pasta Downloads do computador: não há formulários respondidos, mensagens, anotações, gravações nem capturas de avaliadores. Portanto:
- **Pontos positivos relatados por usuários:** nenhum registrado.
- **Problemas identificados por usuários:** nenhum registrado.
- **Sugestões recebidas:** nenhuma registrada.
- **Notas de qualidade (1–5):** nenhuma.

## 7. Problemas e correções (origem técnica)
Falhas encontradas pela equipe e já tratadas: F01, F02, H01, H02, H03 (`docs/07-pendencias.md`, `docs/04-testes.md`). Nenhuma falha de origem humana até o momento.

## 8. Limitações da avaliação
- Seção C não executada.
- Navegador único (Chrome); sem Firefox, Safari ou celular físico.
- Sem testes de componentes React isolados, de carga ou de concorrência (L01).
- Limitações do produto: sem autenticação, fuso, horário de funcionamento ou paginação (L02–L04).

## 9. Conclusão acadêmica (provisória)
Tecnicamente, o MVP atende aos requisitos funcionais implementados, com 28 testes de API e 16 cenários E2E aprovados e 98% de cobertura de linhas no backend. A conclusão sobre a qualidade percebida por usuários **não pode ser emitida**: depende dos cinco laudos reais. Esta seção deve ser reescrita após o recebimento deles.

## 10. Como concluir
1. Distribuir `docs/laudos/INSTRUCOES-AVALIADORES.md` e os formulários a cinco pessoas reais, com consentimento.
2. Receber os formulários preenchidos pelos próprios avaliadores (sem preenchimento pela equipe).
3. Incorporar cada registro ao laudo correto, registrar falhas em `docs/07-pendencias.md` e atualizar as seções 6, 7 e 9 acima.
4. Gerar o PDF consolidado final (capa, introdução, metodologia, resultados, cinco laudos, discussão, conclusão, referências), sem assinaturas artificiais.
