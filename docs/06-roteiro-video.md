# Roteiro operacional do vídeo (~5 min)

Peso na avaliação: 30%. Tudo o que aparecer deve ser real (aplicação rodando, testes executados ao vivo ou saídas reais de `docs/evidencias/`). Dados fictícios apenas.

## Preparação (fazer imediatamente antes de gravar)
Os dados do seed são relativos à **data em que o seed roda**; por isso, reinicie o banco de demonstração no dia da gravação e depois de cada ensaio (o ensaio cria dados).

```powershell
# 1) parar a API (Ctrl+C no terminal dela) e então:
cd backend
Remove-Item agendapro.db        # apaga SOMENTE o banco de demonstração (já recriado pelo seed abaixo)
.venv\Scripts\python.exe -m app.seed
.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000
# 2) em outro terminal
cd frontend
npm run dev                      # http://127.0.0.1:5173
```
Resultado esperado do dashboard logo após o seed: 2 agendamentos hoje, 6 nos próximos 7 dias, 8 ativos, 2 cancelados (20%), receita prevista R$ 460,00, 6 clientes, 4 serviços.
Checklist técnico: janela do navegador em 1280×800 (ou tela cheia 1080p), zoom 100%, sem abas/notificações pessoais visíveis, dois terminais abertos para a parte de testes (`backend` e `frontend`), fonte do terminal grande.

## Roteiro (tempos acumulados)
| Tempo | Cena | Ação na tela | Narração (resumo, falar em ritmo calmo) |
|---|---|---|---|
| 0:00–0:25 | **1. Apresentação** | Slide/README com o nome do projeto, integrantes e disciplina | "Este é o AgendaPro, um sistema de agendamentos para um pequeno estabelecimento com um profissional. Projeto Integrador Transdisciplinar em Engenharia de Software II." |
| 0:25–0:50 | Escopo | README, seção de regras | "O MVP cobre clientes, serviços, agendamentos com remarcação e cancelamento, bloqueio de conflito e dashboard. Ficaram de fora pagamentos, notificações, integrações, IA e login." |
| 0:50–1:20 | **2. Dashboard** | Aba **Dashboard** | "Estes indicadores vêm do banco: agendamentos de hoje, próximos sete dias, ativos, cancelados e taxa, receita prevista e os próximos compromissos." |
| 1:20–1:55 | **3. Cadastro de cliente** | Aba **Clientes** → "+ Novo cliente" → Salvar vazio (mostrar os 3 erros) → preencher "Gustavo Demo", `gustavo@exemplo.test`, `(11) 98888-1111` → Salvar | "Os formulários validam nome, e-mail e telefone, no front e na API. Depois de salvar o cliente aparece na lista." |
| 1:55–2:25 | **4. Cadastro de serviço** | Aba **Serviços** → "+ Novo serviço" → "Hidratação", duração 45, preço `90,50` → Salvar | "O serviço tem duração e preço. A duração define o horário de término dos agendamentos." |
| 2:25–2:50 | **5. Criar agendamento** | Aba **Agendamentos** → "+ Novo agendamento" → cliente Gustavo Demo, serviço *Corte de cabelo*, **amanhã às 10:00** → Salvar | "O sistema calcula o fim: 10:00 às 10:30. O agendamento fica com status Agendado." |
| 2:50–3:15 | **6. Conflito rejeitado** | "+ Novo agendamento" → Gustavo, *Corte de cabelo*, **amanhã às 09:30** → Salvar (sobrepõe o horário 09:00–10:00 da Ana) → mostrar a mensagem → Cancelar o modal | "Como já existe um agendamento nesse intervalo, o sistema recusa e nada é gravado. Horários encostados são permitidos." |
| 3:15–3:40 | **7. Remarcar e cancelar** | No agendamento do Gustavo: "Remarcar" → **amanhã 10:30** → Remarcar; depois "Cancelar" → confirmar | "Remarcar revalida o conflito e mantém a duração. Cancelar libera o horário." |
| 3:40–4:05 | Persistência e celular | Parar e iniciar a API (ou recarregar a página) e mostrar os dados; reduzir a janela para largura de celular | "Os dados estão no SQLite e permanecem após reiniciar. O layout se adapta ao celular." |
| 4:05–4:30 | **8. Arquitetura** | `docs/02-modelo-dados.md` (DER) e árvore `backend/app` | "Back-end FastAPI em camadas: rotas, serviços com as regras, repositórios e modelos SQLAlchemy. Front-end React com TypeScript. Três entidades: clientes, serviços e agendamentos." |
| 4:30–4:50 | **Resultados dos testes** | Terminal: `cd backend` → `python -m pytest -q --cov=app` (≈ 5 s); mostrar "28 passed" e a cobertura. Em seguida, mostrar `docs/evidencias/e2e-saida.txt` (16 passed) ou rodar `npm run e2e` no terminal do front (≈ 20 s) | "Executamos 28 testes de API, com 98% de cobertura de linhas, e 16 testes de ponta a ponta no navegador contra a API real. Os resultados completos estão no repositório." |
| 4:50–5:15 | **9. Conclusão** | Tela do repositório/README e [07-pendencias.md](07-pendencias.md) | "Limitações: sem login e sem horário de funcionamento. A validação com cinco usuários reais ainda depende dos laudos preenchidos. Obrigado." |

Se os 5 laudos já estiverem preenchidos até a gravação, substitua a frase sobre validação por um resumo **fiel** deles. Se não estiverem, diga que estão pendentes; não cite resultados inexistentes.

## Dicas de gravação
- Faça um ensaio completo, depois **reinicie o banco** (comandos acima) antes da gravação final.
- Se errar no meio, prefira regravar a cena em vez de editar resultados.
- A demonstração usa "amanhã" porque o seed coloca ali o horário 09:00–10:00 (Ana) e 11:00–13:00 (Fábio); 10:00–11:00 está livre.
- Duração alvo: 4:30 a 5:30. Exporte em MP4 1080p e confira o áudio antes de enviar.
