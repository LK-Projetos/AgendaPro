# Relatório de montagem — vídeo FINAL_REVISADA (2026-11-17)

Resultado: `AgendaPro_Apresentacao_FINAL_REVISADA.mp4`, arquivo **local e não versionado** (mídia nunca vai ao Git).
Medido: 300,000 s · 9000 quadros · H.264 1280x720 30 fps · AAC 48 kHz estéreo · −15,9 LUFS, pico real −1,3 dBFS.
Situação: **produzido, aguardando a homologação pessoal do autor.** Sem dados pessoais neste relatório.

## Fontes
| Papel | Origem |
|---|---|
| Voz e telas das partes inicial e final | Vídeo original de 5:00 (arquivo local; nunca alterado) |
| Demonstrações (conflito, remarcação, cancelamento) | Gravação de tela de 4:19 feita em 2026-11-17 sobre o banco de demonstração |
| Imagem do GitHub e do Pytest | Duas gravações de tela de 2026-11-17 (somente vídeo; o áudio delas não foi usado) |
| Capturas reais complementares | Páginas `docs/02-modelo-dados.md` e `docs/evidencias/e2e-saida.txt` no GitHub, fotografadas com Chrome/Playwright em 2026-11-17 |
| Descartada | Gravação de 5,6 s (só roteiro em um chat) |

## Timeline final
| Final | Conteúdo | Origem |
|---|---|---|
| 0:00,0–0:30,5 | Apresentação e objetivo | original 0:00–0:30,5 |
| 0:30,5–0:48,4 | Dashboard e indicadores | original 0:35,4–0:53,3 |
| 0:48,4–1:12,5 | Fim do dashboard, Clientes, novo cliente | original 0:59,5–1:23,7 |
| 1:12,5–1:17,0 | Cliente cadastrado | original 1:34,0–1:38,5 |
| 1:17,0–1:33,1 | CRUD básico, Serviços | original 1:48,7–2:04,8 |
| 1:33,1–1:37,0 | Cadastro de serviço | original 2:10,5–2:14,4 |
| 1:37,0–2:37,0 | Serviço com validação de duração, novo agendamento | original 2:19,3–3:19,2 |
| 2:37,0–2:59,5 | Agendamento criado, papel do microempreendedor | original 3:30,3–3:52,8 |
| 2:59,5–3:20,1 | **Conflito de horário** (mensagem real da API) | demonstrações |
| 3:20,1–3:34,2 | **Remarcação** (aviso "Agendamento remarcado.") | demonstrações |
| 3:34,2–3:52,8 | **Cancelamento** com confirmação e status Cancelado | demonstrações |
| 3:52,8–4:20,8 | Tecnologias, com README/Stack no GitHub (voz original) | original + gravação do GitHub |
| 4:20,8–4:29,5 | 28 testes do back-end: Pytest "28 passed", TOTAL 98% | original + gravação do Pytest |
| 4:29,5–4:35,7 | 16 testes ponta a ponta: `e2e-saida.txt` "16 passed" | original + captura real |
| 4:35,7–4:52,8 | Modelagem e conclusão: diagrama de classes de `02-modelo-dados.md` | original + captura real |
| 4:52,8–5:00,0 | Fecho e agradecimento | original 4:52,8–5:00 |

## Cortes aplicados (em pausas reais da fala, sem acelerar)
| Corte | Origem removida | Conteúdo |
|---|---|---|
| a | 0:30,5–0:35,4 | tropeço e frase repetida |
| b | 0:53,3–0:59,5 | detalhe repetido dos próximos agendamentos |
| c | 1:23,7–1:34,0 | **telefone falado em voz alta** e digitação (removido por inteiro, áudio e imagem) |
| d | 1:38,5–1:48,7 | comentário solto e repetição de CRUD |
| e | 2:04,8–2:10,5 | exemplos já cadastrados |
| f | 2:14,4–2:19,3 | digitação do nome do serviço |
| g | 3:19,2–3:30,3 | observação digitada e "Salvar" |
Total removido: 53,3 s, usados integralmente nas demonstrações.

## Privacidade
- Recorte da área do AgendaPro (barra de endereço, favoritos, barra lateral de abas e janelas alheias ao app ficam fora do quadro); barra lateral expandida dos primeiros 30 s coberta.
- Desfoque do e-mail e do telefone do cliente de teste nos diálogos e nas listas.
- Janelas de mensageria e o Explorador de Arquivos presentes nas gravações brutas não foram usados.
- A transcrição local do vídeo final não contém o telefone. Transcrições de trabalho não são versionadas.

## Áudio
Passa-altas 80 Hz, redução leve de ruído, fades de 40 ms nas emendas e `loudnorm` de duas passagens (alvo −16 LUFS, pico −1,5 dB) por grupo de fonte. Resultado −15,9 LUFS, LRA 4,3 LU, sem clipping. Todas as emendas caem em silêncio (≤ −51 dB), exceto a do corte f, mais apertada (pausa de 80 ms).

## Ressalvas
1. Não houve revisão humana do áudio; a transcrição automática (Whisper pequeno) erra palavras. O autor deve assistir ao vídeo inteiro, em especial as emendas em 0:30, 1:37 e 2:59.
2. A tentativa de remarcação em data passada (gravada) ficou de fora para caber nos 300 s.
3. A demonstração de conflito começa em "…e 45" (perde o "às 10").
4. Falas incorretas do original: "Flash API" (o certo é FastAPI), "Playwriter", "credo/crudzão". Só regravando.
5. Remarcação e cancelamento usaram o agendamento nº 5 do seed (não o do roteiro). Os dados do seed são relativos à data de execução.
6. Metadado de proporção (SAR) com desvio de ~0,1%, sem efeito visível.
