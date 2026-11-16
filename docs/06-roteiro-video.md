# Roteiro operacional do vídeo (máximo 5 min; alvo 4:50)

Peso na avaliação: 30%. Tudo o que aparecer deve ser real: aplicação rodando, testes executados ao vivo ou saídas reais de `docs/evidencias/`. Dados fictícios apenas. A narração deve ser gravada por vocês; os textos abaixo são só um guia.

## Preparação (antes de gravar)
O ambiente de demonstração já foi preparado com o seed fictício. Os horários do seed são relativos à **data em que o seed rodou**; se a gravação for em outro dia, ou depois de um ensaio (que cria dados), reinicie o banco de **demonstração** (`backend/agendapro.db`, que só contém dados fictícios do seed; não é versionado):

```powershell
# 1) parar a API (Ctrl+C no terminal dela), então:
cd backend
Remove-Item agendapro.db         # apaga somente o banco de demonstração
.venv\Scripts\python.exe -m app.seed
.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000
# 2) em outro terminal
cd frontend
npm run dev                       # http://127.0.0.1:5173
```
Estado esperado logo após o seed: 2 agendamentos hoje, 6 nos próximos 7 dias, 8 ativos, 2 cancelados (20%), receita prevista R$ 460,00, 6 clientes, 4 serviços.

Checklist de tela: navegador a 1280×800 (ou tela cheia 1080p), zoom 100%, sem abas ou notificações pessoais; dois terminais prontos (`backend` e `frontend`) com fonte grande; documentos abertos em abas: README, `docs/02-modelo-dados.md`, `docs/evidencias/e2e-saida.txt`.

## Sequência (tempos acumulados)
| Tempo | Cena | Ação na tela | Guia de narração |
|---|---|---|---|
| 0:00–0:20 | **1. Apresentação** | README: nome, integrantes, disciplina | AgendaPro, sistema de agendamentos para um estabelecimento com um profissional. Escopo: clientes, serviços, agenda com conflito, dashboard. Fora: pagamentos, notificações, IA, login. |
| 0:20–0:45 | **2. Dashboard** | Aba **Dashboard** | Indicadores calculados do banco: hoje, 7 dias, ativos, cancelados, receita prevista, próximos compromissos. |
| 0:45–1:15 | **3. Cadastro de cliente** | **Clientes** → "+ Novo cliente" → Salvar vazio (3 erros) → "Gustavo Demo", `gustavo@exemplo.test`, `(11) 98888-1111` → Salvar | Validação no front e na API; cliente aparece na lista. |
| 1:15–1:40 | **4. Cadastro de serviço** | **Serviços** → "+ Novo serviço" → "Hidratação", 45 min, `90,50` → Salvar | Duração define o horário de término; preço aceita vírgula. |
| 1:40–2:05 | **5. Criar agendamento** | **Agendamentos** → "+ Novo agendamento" → Gustavo Demo, *Corte de cabelo*, **amanhã 10:00** → Salvar | Término calculado: 10:30. Status Agendado. |
| 2:05–2:30 | **6. Conflito rejeitado** | "+ Novo agendamento" → Gustavo, *Corte de cabelo*, **amanhã 09:30** → Salvar → mostrar a mensagem → Cancelar o modal | Sobrepõe 09:00–10:00 (Ana); o sistema recusa e não grava. Horários encostados são permitidos. |
| 2:30–2:55 | **7. Remarcar e cancelar** | Agendamento do Gustavo: "Remarcar" → **amanhã 10:30** → Remarcar; depois "Cancelar" → confirmar | Remarcar revalida o conflito; cancelar libera o horário. |
| 2:55–3:15 | **8. Persistência e celular** | Recarregar a página (ou reiniciar a API) e mostrar os dados; reduzir a janela à largura de celular | Dados no SQLite; layout responsivo. |
| 3:15–3:45 | **9. Arquitetura** | `docs/02-modelo-dados.md` (DER) e árvore `backend/app` | FastAPI em camadas: rotas, serviços (regras), repositórios, modelos SQLAlchemy; React + TypeScript; três entidades. |
| 3:45–4:25 | **10. Resultados dos testes** | Terminal do back: `python -m pytest -q --cov=app` (≈ 5 s) → "28 passed", 98%. Depois abrir `docs/evidencias/e2e-saida.txt` (16 passed) — **ou** rodar `npm run e2e` (≈ 20 s) se houver tempo | 28 testes de API com 98% de cobertura de linhas e 16 testes de ponta a ponta contra a API real. Resultados completos no repositório. |
| 4:25–4:50 | **11. Conclusão** | README/GitHub e `docs/07-pendencias.md` | Limitações: sem login e sem horário de funcionamento. Validação com 5 usuários: dizer a situação **real** no momento da gravação. |

Se os 5 laudos já estiverem preenchidos por pessoas reais, resuma-os fielmente; se não, diga que estão pendentes. Não cite resultados inexistentes.

## Evidências para mostrar (todas reais, já no repositório)
| O que mostrar | Arquivo |
|---|---|
| 28 testes de API e cobertura | `docs/evidencias/pytest-saida.txt` |
| 16 testes E2E | `docs/evidencias/e2e-saida.txt` |
| Build do front | `docs/evidencias/frontend-build.txt` |
| Persistência após reinício | `docs/evidencias/persistencia-reinicio.txt` |
| Capturas (dashboard, telas, conflito, cancelamento) | `docs/evidencias/capturas/` |

## Dicas
- Faça um ensaio completo e **reinicie o banco** (comandos acima) antes da gravação final.
- Se errar uma cena, regrave a cena; não edite resultados.
- A demonstração usa "amanhã" porque o seed coloca ali 09:00–10:00 (Ana) e 11:00–13:00 (Fábio); 10:00–11:00 está livre.
- Duração máxima 5:00. Cronometre o ensaio e corte a parte de testes ao vivo (use só o arquivo de evidência) se passar do limite.
- Exporte em MP4 1080p, confira o áudio e o formato exigido pelo AVA antes de enviar.
