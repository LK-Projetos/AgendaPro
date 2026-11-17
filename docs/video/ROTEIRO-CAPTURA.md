# Roteiro operacional de captura — 4 clipes

Complementa [PLANO-REVISAO-VIDEO.md](PLANO-REVISAO-VIDEO.md). Você grava a sua própria voz; nada aqui é narração gerada. Os textos de fala são sugestões: use as suas palavras, mantendo o conteúdo e a duração.

## 0. Validação feita antes da gravação (2026-11-17 18:56)
| Verificação | Resultado |
|---|---|
| API e interface | no ar: API `127.0.0.1:8000`, interface **`http://localhost:5173`** |
| 19/11/2026 | só existe Carla Demo, Barba, **10:30–11:00** (nº 9, agendado). Tentar 10:45 com Barba (30 min) ocupa 10:45–11:15 e **conflita** |
| 20/11/2026 | só existe Elisa Modelo, Corte de cabelo, **14:00–14:30** (nº 12, agendado). **15:00–15:30 está livre** |
| Pytest hoje | `28 passed`, cobertura **98%**, 2 s; usa banco em memória e **não toca o banco de demonstração** |
| GitHub | https://github.com/LK-Projetos/AgendaPro responde (público); `origin/main` = `3e33ff6`, que contém README, `docs/` e `docs/evidencias/` |
| Banco | alterado só pela criação do agendamento nº 12 pela API. Cópia anterior intacta em `backend/agendapro.pre-regravacao.db`; vídeo original intacto em Downloads |

Nenhum dado foi alterado direto no banco; nada foi simulado. O conflito não grava nada (a API recusa).

## 1. Antes de apertar REC (vale para os quatro clipes)
1. Resolução da gravação 1280×720, 30 fps, mesmo gravador e mesmo layout do vídeo original (webcam no canto inferior esquerdo, tema escuro, zoom 100%).
2. Microfone perto da boca, fone sem tocar no microfone; teste 10 s e confira que o volume aparece bem alto no medidor (o original ficou baixo).
3. Feche mensagens, notificações e outras janelas. Para os clipes 1–3, abra só `http://localhost:5173` na aba Agendamentos.
4. **Não abra a aba Clientes** em nenhum clipe (há e-mail e telefone de teste cadastrados no banco de casa).
5. Salve os arquivos em `docs/video/clipes/` (pasta ignorada pelo Git; crie-a se não existir).
6. Regra de início e fim: comece a gravar, fique parado e em silêncio por **2 s**, faça o clipe, fique parado por **2 s** e pare. Eu corto essas margens.
7. Fale em ritmo normal. Se errar, **não apague**: recomece a frase e continue. Mande todos os takes.

## 2. Clipe 1 — Conflito de horário
**Arquivo:** `clipe-1-conflito.mp4` · **Duração-alvo:** 20 s (aceitável 18–24 s)

| Passo | O que fazer |
|---|---|
| Iniciar | Aba **Agendamentos** aberta, lista visível, incluindo a linha de **19/11/2026, 10:30 · Carla Demo · Barba**. REC; 2 s parado. |
| 1 | Clicar em **+ Novo agendamento** (canto superior direito da lista). |
| 2 | **Cliente:** Bruno Teste. **Serviço:** Barba (30 min). **Data e hora:** 19/11/2026 10:45 (digite `19112026` e `1045`). **Observações:** deixar vazio. |
| 3 | Clicar em **Salvar**. |
| 4 | Aparece em vermelho no próprio formulário: **"Horário indisponível: já existe um agendamento neste intervalo."** Deixe na tela por 4 s. |
| 5 | Clicar em **Cancelar** (botão do formulário). A lista continua sem novo registro. |
| Encerrar | 2 s parado e parar a gravação. |

**Narração (≈ 18 s):** "Agora a regra mais importante. Já existe um agendamento de Carla Demo, das 10:30 às 11:00. Se eu tento marcar outro cliente às 10:45, o sistema recusa com esta mensagem e não salva nada. Assim a agenda nunca tem dois clientes no mesmo horário."

## 3. Clipe 2 — Remarcação
**Arquivo:** `clipe-2-remarcacao.mp4` · **Duração-alvo:** 17 s (aceitável 15–21 s)

| Passo | O que fazer |
|---|---|
| Iniciar | Aba **Agendamentos**, linha **20/11/2026, 14:00 · Elisa Modelo · Corte de cabelo** visível. REC; 2 s parado. |
| 1 | Na linha da Elisa Modelo, clicar em **Remarcar**. |
| 2 | **Novo horário:** 20/11/2026 15:00 (`20112026` e `1500`). |
| 3 | Clicar em **Remarcar** (botão azul do formulário). Aparece o aviso **"Agendamento remarcado."** |
| 4 | Apontar com o mouse a linha com **15:00**. |
| Encerrar | 2 s parado e parar a gravação. |

**Narração (≈ 15 s):** "Para remarcar, clico em Remarcar na linha do agendamento e escolho um novo horário livre. O agendamento da Elisa passa das 14:00 para as 15:00, e o horário antigo volta a ficar livre."

Se errar e precisar repetir: remarque de volta para 14:00 **fora da gravação** e regrave.

## 4. Clipe 3 — Cancelamento
**Arquivo:** `clipe-3-cancelamento.mp4` · **Duração-alvo:** 17,5 s (aceitável 15–21 s) · Grave **logo depois do clipe 2**, com a Elisa às 15:00.

| Passo | O que fazer |
|---|---|
| Iniciar | Aba **Agendamentos**, linha **20/11/2026, 15:00 · Elisa Modelo** (status Agendado). REC; 2 s parado. |
| 1 | Na linha da Elisa Modelo, clicar em **Cancelar**. |
| 2 | Surge a janela do navegador **"Cancelar o agendamento de Elisa Modelo em …?"**. Deixe visível por 2 s e clique em **OK**. |
| 3 | Aparece **"Agendamento cancelado."** e o status passa a **Cancelado**. Aponte o status por 3 s. |
| Encerrar | 2 s parado e parar a gravação. |

**Narração (≈ 15 s):** "Para cancelar, o sistema pede confirmação. Ao confirmar, o agendamento passa para Cancelado e o horário volta a ficar livre para outro cliente."

**Atenção:** o cancelamento não tem como ser desfeito. Se precisar regravar, me avise: crio outro agendamento-base pela API (nº 13) e você repete. Confirme que a janela de confirmação do navegador aparece no vídeo; se o gravador capturar só a janela do navegador e ela sumir, regrave capturando a tela inteira.

## 5. Clipe 4 — Evidências (GitHub, arquitetura, testes), SEM narração
**Arquivo:** `clipe-4-evidencias-tela.mp4` · **Duração-alvo:** 70 s (aceitável 65–80 s)

Esta imagem será colocada sobre a sua fala original da seção "tecnologia e testes" (3:54–5:00). **Não fale durante este clipe**; deixe o microfone mudo. Faça uma janela limpa: navegador em perfil Convidado, favoritos e painel de abas ocultos. Para o terminal, use uma janela sem outros assuntos visíveis.

| Bloco | Duração | O que mostrar (nesta ordem, devagar) |
|---|---|---|
| A | 20 s | https://github.com/LK-Projetos/AgendaPro → rolar até a seção **Stack** do README (React, TypeScript, FastAPI, SQLAlchemy, SQLite, Pytest) e depois **Estrutura** (backend/app, frontend/src, docs). |
| B | 15 s | Abrir `docs/02-modelo-dados.md` no GitHub e rolar os diagramas (classes e DER). Em seguida, voltar e abrir `docs/evidencias`. |
| C | 20 s | Terminal na pasta `backend` do projeto. Digitar: `.\.venv\Scripts\python.exe -m pytest -q --cov=app` e Enter. Esperar terminar (≈ 2–6 s) e deixar 6 s parado em **"28 passed"** e **"TOTAL … 98%"**. |
| D | 15 s | Abrir `docs/evidencias/e2e-saida.txt` (no GitHub ou no editor) e deixar 6 s parado na linha **"16 passed"**. |

Entre os blocos, 2 s de pausa. Não abra `docs/laudos` nem a aba Clientes do sistema.

## 6. Ordem de gravação sugerida
1) Clipe 1, 2) Clipe 2, 3) Clipe 3 (continuam o estado do banco), 4) Clipe 4.
Quando terminar, me avise com o nome dos arquivos. Eu integro ao original, normalizo o áudio, aplico o recorte de privacidade e exporto `AgendaPro_Apresentacao_FINAL_REVISADA.mp4` com 300,000 s, junto com o relatório de validação, **antes de pedir qualquer autorização de commit ou push**.

## 7. Cortes aprovados no original e privacidade
- Aprovados: todos os cortes a–g do plano, **somente** pausas, tropeços, repetições e trechos redundantes. As explicações técnicas e a naturalidade da fala são preservadas; cortes sempre em pontos de respiração entre frases.
- A transcrição fica **apenas local** e é ignorada pelo Git (`docs/video/transcricao-original.md`). Não é publicada.
