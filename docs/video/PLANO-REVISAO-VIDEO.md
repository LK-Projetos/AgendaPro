# Plano de revisão do vídeo — AgendaPro (versão FINAL_REVISADA)

**Status em 2026-11-17 (atualizado após a montagem)**
- **Vídeo revisado produzido** (300,000 s, 9000 quadros), arquivo local não versionado. **Aguarda a homologação pessoal do autor.** Resultado, timeline real e ressalvas: [RELATORIO-CORTES.md](RELATORIO-CORTES.md).
- Vídeo original gravado, **5:00 exatos**, preservado (local, não versionado).
- Auditoria que originou o plano: a demonstração das **regras de negócio** (conflito, remarcação, cancelamento) estava ausente. Resolvida na versão revisada.
- Corte de privacidade do telefone falado: **aprovado e aplicado**. Demais cortes (a, b, d, e, f, g): **aprovados e aplicados**, em pausas reais da fala (os tempos exatos diferem dos aproximados abaixo; ver o relatório).
- Os "4 clipes complementares" foram substituídos por gravações livres de 2026-11-17 (demonstrações, GitHub e Pytest) e por capturas reais de `02-modelo-dados.md` e `e2e-saida.txt`. O roteiro previsto está em [ROTEIRO-CAPTURA.md](ROTEIRO-CAPTURA.md) (histórico).
- Continuidade em outro computador: [HANDOFF-OUTRO-COMPUTADOR.md](HANDOFF-OUTRO-COMPUTADOR.md). Os IDs e datas citados no texto abaixo (nº 12, 19 e 20/11) eram do banco local de casa e **não existem em outro computador**; o plano a seguir é o planejamento original, mantido como histórico.

Original (preservado, nunca alterado; fica só no computador de casa e não é versionado): `AgendaPro_Apresentacao_Final_05min.mp4` — 1280×720, 30 fps, H.264 + AAC 48 kHz estéreo, 300,000 s.
Saída: `AgendaPro_Apresentacao_FINAL_REVISADA.mp4`, MP4/H.264/AAC, 1280×720, **300,000 s** (9000 quadros a 30 fps).
Transcrição automática do original: arquivo **local e não versionado** (`docs/video/transcricao-original.md`, ignorado pelo Git por conter dados do vídeo). Para refazer, ver [HANDOFF-OUTRO-COMPUTADOR.md](HANDOFF-OUTRO-COMPUTADOR.md).

> **Correção em relação à versão anterior deste plano:** a detecção de silêncio indicou "pausas" de 19, 43 e 32 s, mas a transcrição mostra que **a fala é contínua** (0:00 a 4:59). O áudio é baixo e o limiar de −45 dB confundiu fala baixa com silêncio. Por isso nenhum trecho será cortado por silêncio: os cortes seguem frases.

## 1. Mapa do original (fala + tela)
| Tempo | Fala | Tela |
|---|---|---|
| 0:00–0:32 | Apresentação (nome, curso, objetivo do projeto) | Dashboard |
| 0:32–1:06 | Indicadores do dashboard | Dashboard |
| 1:06–1:25 | Vai para Clientes e cadastra um cliente de teste | Clientes, digitação |
| 1:25–1:34 | **Diz em voz alta o telefone digitado** | Formulário |
| 1:34–2:05 | Cliente salvo, CRUD, serviços | Clientes → Serviços |
| 2:05–2:55 | Cadastra "Alisamento" e mostra a validação de duração (múltiplos de 15) | Serviços |
| 2:55–3:34 | Novo agendamento (cliente de teste, serviço Alisamento, 17/11) | Agendamentos |
| 3:34–3:54 | "CRUD de agendamento funcionando", papel do microempreendedor | Lista parada |
| 3:54–4:32 | Tecnologia (React/TypeScript, FastAPI, SQLite), tudo local, MVP | Lista parada |
| 4:32–4:51 | **"28 testes do back-end e 16 ponta a ponta"** (Playwright) | Lista parada |
| 4:51–5:00 | Conclusão e agradecimento | Lista parada |

Não há fala nem imagem sobre conflito, remarcação ou cancelamento. A parte final (3:54–5:00) tem conteúdo essencial (stack, testes, conclusão), mas a tela fica parada. **Solução:** manter a sua voz e a sua webcam e trocar só a imagem da tela por gravações reais (GitHub, testes).

## 2. Timeline de 300 s
Cortes propostos no original (a confirmar ouvindo; os pontos finais usam o tempo de cada palavra):
| Corte | Origem | Dur. | Motivo |
|---|---|---|---|
| a | 0:32,2–0:37,2 | 5,0 | Tropeço ("deixa eu melhorar aqui") |
| b | 0:51,2–0:57,6 | 6,4 | Detalhe repetido dos indicadores (está na tela) |
| c | 1:24,6–1:33,7 | 9,1 | **Telefone falado em voz alta** (privacidade) e digitação |
| d | 1:39,5–1:46,5 | 7,0 | Comentário solto ("bonitão já") |
| e | 2:04,6–2:11,7 | 7,1 | Exemplos já cadastrados |
| f | 2:15,6–2:22,4 | 6,8 | Digitação do nome do serviço |
| g | 3:13,1–3:26,0 | 12,9 | Preenchimento do agendamento ("fulano vai vir na parte da…", observação digitada) |

Total cortado ≈ 54,3 s; fica ≈ 245,5 s do original. Sobram **≈ 54,5 s** para as três demonstrações novas.

| # | Origem | Duração | Conteúdo |
|---|---|---|---|
| 1 | Original, 0:00–3:54 menos cortes a–g | ≈ 179,6 | Apresentação, dashboard, clientes, serviços, agendamento criado |
| 2 | **NOVO A+B** (voz nova) | ≈ 20,0 | Tentativa em horário ocupado + mensagem real de rejeição |
| 3 | **NOVO C** (voz nova) | ≈ 17,0 | Remarcação |
| 4 | **NOVO D** (voz nova) | ≈ 17,5 | Cancelamento com confirmação |
| 5 | Original 3:54–5:00 (**voz e webcam originais, imagem trocada**) | ≈ 66,0 | Tecnologia e testes, com a imagem de **GitHub** e dos **testes** gravada em E |

Soma ≈ 299,8 s; os 0,2 s restantes e os acertos finais saem das pausas dentro dos clipes novos, nunca de acelerar a fala. A faixa 5 usa imagem nova sobre a sua fala original; a webcam do original continua sincronizada.

Imagem da faixa 5: 3:54–4:15 repositório GitHub (README com a stack) · 4:15–4:32 pasta `docs/evidencias` ou terminal · 4:32–4:51 Pytest "28 passed" e `e2e-saida.txt` "16 passed" · 4:51–5:00 volta ao app ou ao repositório.

## 3. Preparação feita (computador de casa; não vale automaticamente em outro computador)
- API em http://127.0.0.1:8000 e interface em **http://localhost:5173** (o Vite não responde em 127.0.0.1 nesta máquina). Terminais "API 8000" e "Front 5173" no painel.
- Banco de demonstração intocado. Cópia de segurança antes da regravação: `backend/agendapro.pre-regravacao.db` (ignorada pelo Git). Para voltar: pare a API e copie o arquivo de volta sobre `backend/agendapro.db`.
- Agendamentos futuros hoje: 19/11 10:30–11:00 (Carla Demo, Barba) e 21/11 16:00 (Diego Fictício). Os de 13 a 17/11 já são passados.
- **Privacidade:** o banco de casa tem um cliente de teste cadastrado durante a gravação (com e-mail e telefone digitados). Não abra a aba **Clientes** nas gravações novas. Nos trechos antigos, e-mail e telefone serão desfocados.

## 4. Roteiro de captura (grave a tela inteira, no mesmo layout do original)
Regras gerais: 1280×720, webcam no mesmo canto, tema escuro, zoom 100%, microfone próximo (o original ficou baixo). Pausa de 1 s antes e depois de cada ação. Se errar, repita e envie todos os takes. Os diálogos de confirmação do cancelamento são do navegador: confira que a gravação os captura.

**Base já criada (ação real na API):** "Elisa Modelo, Corte de cabelo, 20/11/2026 14:00" (se gravar depois de 20/11, crie outra com data futura). O conflito usa o agendamento já existente de 19/11 10:30 (Carla Demo, Barba); se gravar depois de 19/11, use esse mesmo passo com a base da Elisa (14:00–14:30) e tente 14:15.

**Clipe A+B — conflito (alvo 20 s)** — `novo-A-conflito.mp4`
Aba Agendamentos → "+ Novo agendamento": Bruno Teste, Barba, 19/11/2026 **10:45** → Salvar. Deixe a mensagem **"Horário indisponível: já existe um agendamento neste intervalo."** por 4 s; Cancelar o formulário; mostre a lista sem novo registro.
*Fala (≈ 18 s):* "Agora a regra principal. Já existe um agendamento das 10:30 às 11:00. Se eu tento marcar outro às 10:45, o sistema recusa com esta mensagem e não salva nada. A agenda nunca fica com dois clientes no mesmo horário."

**Clipe C — remarcação (alvo 17 s)** — `novo-C-remarcacao.mp4`
Linha da Elisa Modelo (20/11 14:00) → Remarcar → 20/11/2026 **15:00** → Salvar. A lista mostra 15:00.
*Fala (≈ 15 s):* "Para remarcar, uso o botão Remarcar e escolho um novo horário livre. O agendamento passa para as 15:00, e o horário antigo fica liberado."

**Clipe D — cancelamento (alvo 17,5 s)** — `novo-D-cancelamento.mp4`
Mesma linha (agora 15:00) → Cancelar → deixe o diálogo "Cancelar o agendamento de Elisa Modelo em …?" visível por 2 s → OK. Status "Cancelado".
*Fala (≈ 15 s):* "Para cancelar, o sistema pede confirmação. Ao confirmar, o status passa para Cancelado e o horário volta a ficar livre."

**Clipe E — imagem de apoio, SEM narração (≈ 70 s de gravação de tela)** — `novo-E-tela-github-testes.mp4`
Grave em janela de navegador limpa (perfil Convidado, favoritos e painel de abas ocultos), em silêncio, em quatro blocos com 3 s de pausa entre eles:
1. (20 s) https://github.com/LK-Projetos/AgendaPro: README, depois as pastas `backend`, `frontend`, `docs`.
2. (15 s) Pasta `docs/evidencias` no GitHub.
3. (20 s) Terminal em `backend`: `.\.venv\Scripts\python.exe -m pytest -q --cov=app` (cerca de 6 s). Deixe na tela "28 passed" e "TOTAL … 98%".
4. (15 s) Arquivo `docs/evidencias/e2e-saida.txt` com "16 passed" (no editor ou no GitHub).
Não use sua voz nesse clipe: vale a fala do original.
Observação (situação na data do plano, já superada): o GitHub (`origin/main`) estava em `3e33ff6` e o commit local `592c000` ainda não tinha sido enviado; hoje a documentação está publicada (ver `git log`). Os laudos lá são formulários em branco; mesmo assim, evite abrir `docs/laudos`.

## 5. Decisões
1. **Aprovado:** cortar o telefone falado em voz alta (corte c).
2. **Feito em 2026-11-17:** base criada pela API real: agendamento nº 12, Elisa Modelo, Corte de cabelo, 20/11/2026 14:00–14:30. Os clipes C e D usam esse registro.
3. **Aprovados** os cortes a, b, d, e, f, g, **somente** se forem pausas, tropeços, repetições ou trechos redundantes; as explicações técnicas e a naturalidade da fala devem ser preservadas.
4. E-mail e telefone do cliente de teste aparecem na tela do original; serão desfocados mesmo sendo fictícios.

## 6. Edição (após receber os arquivos)
- **Privacidade:** recorte da área do aplicativo (x 160–1280, y 58–720), eliminando barra de endereço, favoritos e abas laterais, com escala a 720p e barras laterais na cor do fundo. Webcam reaplicada no canto inferior esquerdo. Desfoque de e-mail e telefone do cliente de teste onde aparecem.
- **Áudio:** `highpass=f=80`, redução leve de ruído, `loudnorm` em duas passagens (alvo −16 LUFS, pico real −1,5 dB), fades de 0,15 s nas emendas. Sem acelerar a fala.
- **Exportação:** `libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 30`, `aac -b:a 192k -ar 48000`, `-t 300`.
- **Homologação:** `ffprobe` (duração 300,000 e 9000 quadros), `volumedetect`, inspeção visual de cada emenda, confirmação de que conflito, remarcação e cancelamento aparecem, relatório de cortes em `docs/video/RELATORIO-CORTES.md`. O original não é alterado.
