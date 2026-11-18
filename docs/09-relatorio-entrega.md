# Relatório de entrega — AgendaPro (homologação de 2026-11-16; atualizado em 2026-11-17)

**Veredito:** o MVP está tecnicamente homologado e o código e a documentação estão publicados no GitHub (`main`). O vídeo revisado (300 s) foi produzido e **aguarda a homologação pessoal do autor**. A entrega acadêmica **não está concluída**: faltam as 5 avaliações humanas reais (0 de 5), a homologação do vídeo e a submissão no AVA.

## 1. Funcionalidades aprovadas (com evidência de execução real)
| Funcionalidade | Pytest | E2E | Observação |
|---|---|---|---|
| Dashboard com indicadores reais | ✔ | ✔ 01, 15 | |
| CRUD de clientes (+ busca, duplicidade) | ✔ | ✔ 03–06, 14 | |
| CRUD de serviços (preço e duração) | ✔ | ✔ 07–09, 14 | Campo monetário corrigido (H02) |
| CRUD de agendamentos | ✔ | ✔ 02, 10 | |
| Remarcação e cancelamento | ✔ | ✔ 12, 13 | |
| Bloqueio de conflito | ✔ | ✔ 11, 12, 13 | |
| Validação de formulários | ✔ | ✔ 03, 05, 08 | front e back |
| Persistência SQLite | ✔ | ✔ 15 | reinício do processo: [persistencia-reinicio.txt](evidencias/persistencia-reinicio.txt) |
| Tratamento de erros | ✔ | ✔ | formato `{code,message,details}` |
| Dados fictícios | ✔ | ✔ 01, 02 | |
| Layout responsivo | — | ✔ 16 | 375 px sem rolagem horizontal |

## 2. Testes executados
| Teste | Resultado |
|---|---|
| Pytest | 28 passed, 0 failed; cobertura de linhas 98% |
| E2E Playwright (Chrome) | 16 passed, 0 failed (rodado duas vezes seguidas) |
| typecheck / build | OK |
| lint | 1 aviso sem impacto |
| Persistência após reinício da API | OK |

Reexecução de integridade em 2026-11-17 (outro computador): Pytest 28 passed, 98%; Playwright 16 passed; typecheck e build OK. As saídas arquivadas em `docs/evidencias/` são as de 2026-11-16.

## 3. Evidências existentes (`docs/evidencias/`)
`pytest-saida.txt` (inclui cobertura) · `e2e-saida.txt` · `frontend-build.txt` · `persistencia-reinicio.txt` · `validacao-navegador.md` (validação manual anterior, parcialmente superada pelo E2E) · `capturas/` com 10 imagens: dashboard, agendamentos, clientes, serviços, validação de cliente, validação de serviço, **agendamento criado**, **conflito rejeitado**, **cancelamento**, mobile.
O relatório de cobertura em HTML não é versionado; a tabela de cobertura por arquivo está em `pytest-saida.txt`. Para capturas manuais adicionais: abra a aplicação e use a ferramenta de recorte do sistema (Win+Shift+S).

## 4. Pendências reais
| Item | Responsável |
|---|---|
| Homologar o vídeo revisado de 300 s (produzido em 2026-11-17; ver [video/RELATORIO-CORTES.md](video/RELATORIO-CORTES.md)) e decidir sobre falas incorretas do original | Autor |
| Realizar 5 avaliações humanas e preencher os laudos (0 de 5 recebidas) | Avaliadores + equipe (não foram simulados) |
| Registrar falhas relatadas nos laudos em [07-pendencias.md](07-pendencias.md) e corrigir | Equipe |
| Informar nomes da equipe/professor no README e no vídeo | Equipe |
| Submissão no AVA (formato, tamanho e campos exigidos a confirmar) | Equipe |
| Limitações técnicas L01–L08 | ver [07-pendencias.md](07-pendencias.md) |

## 5. Estado do Git
Branch `main`; remoto `origin` = `https://github.com/LK-Projetos/AgendaPro.git`. A publicação inicial foi feita em 2026-11-16 (até `7b76374`, evento histórico); a documentação posterior foi publicada em 2026-11-17 e o estado atual está em `git log`. Nenhum merge ou deploy executado. Auditoria: nenhum `.env`, `.venv`, `node_modules`, banco `*.db`, artefato de teste (`e2e/.tmp`, relatórios) ou segredo versionado; busca por padrões de senha/token/chave em código não retornou ocorrências. Cobertos pelo `.gitignore`: `.venv/`, `.env`, `*.db`, `node_modules`, `dist/`, `e2e/.tmp/`, `e2e/.report/`. O histórico contém os commits de planejamento, MVP e homologação (ver `git log`).

## 6. Comandos para iniciar o MVP
```bash
# Terminal 1
cd backend && python -m venv .venv && .venv\Scripts\Activate.ps1 && pip install -r requirements.txt
python -m app.seed
python -m uvicorn app.main:app --port 8000
# Terminal 2
cd frontend && npm install && npm run dev      # http://127.0.0.1:5173
```
Testes: `cd backend && python -m pytest -v --cov=app` · `cd frontend && npm run e2e`.
(Comandos conferidos no ambiente de desenvolvimento; não foi feita instalação em máquina limpa.)

## 7. Instruções para os cinco avaliadores
[laudos/INSTRUCOES-AVALIADORES.md](laudos/INSTRUCOES-AVALIADORES.md) (roteiro de 9 passos) e templates `laudos/laudo-avaliador-1..5.md`, em branco.

## 8. Prontidão
- **Vídeo: produzido** (300,000 s, 2026-11-17), aguardando a homologação pessoal do autor.
- **Publicação: feita** (código e documentação em `main`).
- **Entrega acadêmica completa: não pronta** (homologação do vídeo, 5 avaliações humanas reais e submissão no AVA pendentes).
