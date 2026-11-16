# Relatório de entrega — AgendaPro (2026-11-16)

**Veredito:** o MVP está tecnicamente homologado e pronto para gravação do vídeo. A entrega acadêmica **não está concluída**: faltam o vídeo, os 5 laudos de avaliadores humanos e a publicação no GitHub.

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

## 3. Evidências existentes (`docs/evidencias/`)
`pytest-saida.txt` (inclui cobertura) · `e2e-saida.txt` · `frontend-build.txt` · `persistencia-reinicio.txt` · `validacao-navegador.md` (validação manual anterior, parcialmente superada pelo E2E) · `capturas/` com 10 imagens: dashboard, agendamentos, clientes, serviços, validação de cliente, validação de serviço, **agendamento criado**, **conflito rejeitado**, **cancelamento**, mobile.
O relatório de cobertura em HTML não é versionado; a tabela de cobertura por arquivo está em `pytest-saida.txt`. Para capturas manuais adicionais: abra a aplicação e use a ferramenta de recorte do sistema (Win+Shift+S).

## 4. Pendências reais
| Item | Responsável |
|---|---|
| Gravar o vídeo (~5 min) com o roteiro em [06-roteiro-video.md](06-roteiro-video.md) | Equipe |
| Realizar 5 avaliações humanas e preencher os laudos | Avaliadores + equipe (não foram simulados) |
| Registrar falhas relatadas nos laudos em [07-pendencias.md](07-pendencias.md) e corrigir | Equipe |
| Enviar ao GitHub os commits posteriores ao push de `7b76374` (publicação inicial já feita) | Equipe, com autorização |
| Informar nomes da equipe/professor no README e no vídeo | Equipe |
| Limitações técnicas L01–L08 | ver [07-pendencias.md](07-pendencias.md) |

## 5. Estado do Git
Branch `main`; remoto `origin` = `https://github.com/LK-Projetos/AgendaPro.git`; publicado até `7b76374` (local = remoto no momento da verificação). Nenhum merge ou deploy executado. Auditoria: nenhum `.env`, `.venv`, `node_modules`, banco `*.db`, artefato de teste (`e2e/.tmp`, relatórios) ou segredo versionado; busca por padrões de senha/token/chave em código não retornou ocorrências. Cobertos pelo `.gitignore`: `.venv/`, `.env`, `*.db`, `node_modules`, `dist/`, `e2e/.tmp/`, `e2e/.report/`. O histórico contém os commits de planejamento, MVP e homologação (ver `git log`).

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
- **Gravação do vídeo: pronta.** Aplicação estável, seed fictício, roteiro e evidências reais disponíveis. Antes de gravar, apagar `backend/agendapro.db` e rodar o seed, para que "hoje" mostre agendamentos futuros.
- **Publicação: feita** (`7b76374`); faltam apenas os commits de documentação posteriores.
- **Entrega acadêmica completa: não pronta** (vídeo e laudos humanos pendentes).
