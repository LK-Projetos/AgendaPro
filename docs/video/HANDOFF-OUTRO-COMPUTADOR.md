# HANDOFF — continuar o AgendaPro em outro computador

Escrito em 2026-11-17 para uma nova sessão do Claude Code retomar sem o histórico da conversa anterior. Caminhos relativos à raiz do repositório; a estrutura de pastas do novo computador pode ser diferente.

## 1. Objetivo acadêmico
AgendaPro é o MVP do Projeto Integrador Transdisciplinar em Engenharia de Software II (Cruzeiro do Sul Virtual). Pesos: código 20%, **vídeo explicativo de 5 min 30%**, teste da solução 25%, **laudos de qualidade com 5 avaliadores humanos reais 25%**. O que falta: vídeo revisado e os 5 laudos reais.

## 2. Stack e estrutura
React 19 + TypeScript + Vite · Python 3.13 + FastAPI · SQLAlchemy 2 + SQLite · Pytest · Playwright.
```
backend/app/    routers/api.py · services.py (regras) · repositories.py · models.py · schemas.py · seed.py · database.py
backend/tests/  Pytest        frontend/src/  pages/ (Dashboard, Clients, Services, Appointments)
frontend/e2e/   Playwright    docs/          requisitos, API, testes, laudos, evidencias, video
```

## 3. Estado do código
MVP funcional e homologado em 2026-11-16 (commit de código `b4252fb`; nada em `backend/` ou `frontend/` mudou depois). Funcionalidades: dashboard; CRUD de clientes, serviços e agendamentos; remarcar; cancelar; bloqueio de conflito (início_A < fim_B e fim_A > início_B; cancelados não bloqueiam; encostar é permitido); validação; persistência; layout responsivo. Regras e limitações: `docs/01-requisitos.md`, `docs/07-pendencias.md`. **Não modifique o código do produto para a gravação.**

## 4. Testes e evidências
- Pytest: 28 aprovados, cobertura de linhas 98% (evidência de 2026-11-16 em `docs/evidencias/pytest-saida.txt`; reexecutado em 2026-11-17 nesta sessão de casa com o mesmo resultado).
- E2E Playwright: 16 aprovados em duas execuções (2026-11-16, `docs/evidencias/e2e-saida.txt`). **Não foi reexecutado depois.**
- Também: `docs/evidencias/frontend-build.txt`, `persistencia-reinicio.txt`, 10 capturas em `docs/evidencias/capturas/`.
- Não afirme novas execuções sem rodá-las. Detalhes e limitações: `docs/04-testes.md`.

## 5. Situação do vídeo
- **Original** gravado pelo autor, 5:00 exatos (1280×720, 30 fps). Arquivo só no computador de casa; não é versionado.
- **Problemas:** não mostra conflito, remarcação nem cancelamento; ~88 s finais com tela parada; áudio baixo (média −35,2 dB); barra do navegador e abas pessoais visíveis; telefone dito em voz alta.
- **Versão revisada: ainda NÃO produzida.** **Os 4 clipes complementares: NÃO gravados.**
- Decisões e timeline completas: [PLANO-REVISAO-VIDEO.md](PLANO-REVISAO-VIDEO.md).

## 6. Cortes aprovados (no vídeo original)
Aprovados pelo autor, **somente** pausas, tropeços, repetições e trechos redundantes; preservar explicações técnicas e a naturalidade da fala; cortar em respiração entre frases; nunca acelerar a fala.
| Corte | Origem | Motivo |
|---|---|---|
| a | 0:32,2–0:37,2 | tropeço |
| b | 0:51,2–0:57,6 | detalhe repetido dos indicadores |
| c | 1:24,6–1:33,7 | **telefone falado em voz alta (privacidade)** e digitação |
| d | 1:39,5–1:46,5 | comentário solto |
| e | 2:04,6–2:11,7 | exemplos já cadastrados |
| f | 2:15,6–2:22,4 | digitação do nome do serviço |
| g | 3:13,1–3:26,0 | preenchimento do agendamento |
Tempos aproximados (vindos de transcrição automática): ajustar os pontos exatos ouvindo o áudio. **Não confie em detecção de silêncio**: a fala é contínua e baixa; um limiar de −45 dB confunde fala com pausa. A tela fica parada de ~3:34 a 5:00 com fala essencial (stack, "28 testes de back-end e 16 ponta a ponta", conclusão): manter a voz e a webcam originais e trocar só a imagem pelo clipe 4.

## 7. Roteiro dos 4 clipes pendentes
Detalhes (cliques, campos, narração, tempos, quando iniciar e parar): [ROTEIRO-CAPTURA.md](ROTEIRO-CAPTURA.md). Resumo, com datas relativas (veja a seção 10 para obtê-las no seu banco):
| # | Arquivo | Alvo | Ação |
|---|---|---|---|
| 1 | `clipe-1-conflito.mp4` | 20 s | Novo agendamento de Bruno Teste, Barba, 15 min depois do início do agendamento futuro de Carla Demo: mensagem "Horário indisponível: já existe um agendamento neste intervalo." |
| 2 | `clipe-2-remarcacao.mp4` | 17 s | Remarcar o agendamento-base de Elisa Modelo (14:00) para 15:00 do mesmo dia |
| 3 | `clipe-3-cancelamento.mp4` | 17,5 s | Cancelar o mesmo agendamento, com a confirmação do navegador (grave logo após o clipe 2) |
| 4 | `clipe-4-evidencias-tela.mp4` | ~70 s | **Sem voz**: GitHub (stack e estrutura do README), `docs/02-modelo-dados.md`, Pytest ao vivo, `docs/evidencias/e2e-saida.txt` |
O autor grava a **própria voz**. Não gere narração artificial nem simule telas, respostas da API ou capturas.

## 8. Instalar e executar no Windows
Requisitos: Python 3.11+, Node 20+, Git, Google Chrome, FFmpeg (com `ffprobe`).
```powershell
git clone https://github.com/LK-Projetos/AgendaPro.git
cd AgendaPro
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd ..\frontend
npm.cmd install
```
Use `npm.cmd` se o PowerShell bloquear `npm.ps1` (política de execução); não altere a política do sistema.

## 9. Banco descartável com dados fictícios
O banco padrão é `backend/agendapro.db` (ignorado pelo Git). Para um banco separado, use a variável `AGENDAPRO_DB_URL`. Crie-o fora do repositório ou em arquivo `.db` (qualquer `*.db` é ignorado):
```powershell
cd backend
$env:AGENDAPRO_DB_URL = "sqlite:///C:/temp/agendapro-gravacao.db"
.\.venv\Scripts\python.exe -m app.seed
.\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000
```
Em outro terminal:
```powershell
cd frontend
npm.cmd run dev
```
Abra **http://localhost:5173** (em algumas máquinas o Vite não atende em 127.0.0.1). O seed é relativo à data de execução (L07 em `docs/07-pendencias.md`), então as datas dos agendamentos mudam por dia. **Não presuma** que o banco de casa existe: o agendamento nº 12, a base de Elisa Modelo e o cliente de teste cadastrado durante a gravação original estão apenas no banco local de casa. Nunca apague um banco que não seja o descartável que você mesmo criou.

## 10. Reproduzir conflito, remarcação e cancelamento (sem IDs fixos)
Com a API no ar:
```powershell
powershell -ExecutionPolicy Bypass -File docs/video/preparar-cenarios.ps1 -Api http://127.0.0.1:8000
```
O script usa a API real: encontra o agendamento futuro de Carla Demo, cria (se não existir) o agendamento-base "Elisa Modelo, Corte de cabelo, dia seguinte ao de Carla, 14:00" e imprime as datas e os horários a usar na interface. Idempotente; não altera o banco diretamente.
Cenários (valide cada um antes de gravar):
1. **Conflito:** Bruno Teste, Barba (30 min), início 15 min após o início de Carla Demo → deve aparecer 409 `SCHEDULE_CONFLICT` com a mensagem acima e nada é criado.
2. **Remarcação:** base de Elisa Modelo de 14:00 para 15:00 (livre) → "Agendamento remarcado.".
3. **Cancelamento:** mesmo agendamento → confirmação do navegador → "Agendamento cancelado." e status Cancelado. **Não é desfeito**; para regravar, rode o script de novo: como o agendamento cancelado não bloqueia horários, ele cria uma nova base no mesmo horário.

## 11. Validar a API e a interface
```powershell
curl.exe -s http://127.0.0.1:8000/api/health        # {"status":"ok"}
curl.exe -s http://127.0.0.1:8000/api/dashboard
curl.exe -s -o NUL -w "%{http_code}" http://localhost:5173
```
Documentação interativa da API: http://127.0.0.1:8000/docs. Testes: na pasta `backend`, `.\.venv\Scripts\python.exe -m pytest -q --cov=app` (cerca de 2 s; usa banco em memória, não toca o banco de gravação). E2E: na pasta `frontend`, `npm.cmd run e2e` (usa API na 8001 e front na 5174 com banco descartável próprio).

## 12. Onde colocar os 4 MP4 e o original
- Clipes gravados: `docs/video/clipes/` com os nomes exatos da seção 7 (a pasta é ignorada pelo Git; crie-a).
- Vídeo original: copie para `docs/video/clipes/original.mp4` ou informe o caminho (também ignorado). **Nunca versionar mídia.**
- Saída final: `docs/video/AgendaPro_Apresentacao_FINAL_REVISADA.mp4` (ignorado pelo Git).

## 13. Retomar a montagem final (300,000 s exatos)
1. `ffprobe` em cada arquivo (resolução, fps, duração, canais). Padronizar tudo para 1280×720, 30 fps, estéreo 48 kHz.
2. Privacidade nos trechos do original: recortar a área do aplicativo (aprox. x 160–1280, y 58–720 do quadro 1280×720), eliminando barra de endereço, favoritos e abas laterais; escalar a 720p com barras laterais na cor do fundo; reaplicar a webcam (aprox. x 52–348, y 378–600) no canto inferior esquerdo; desfocar e-mail e telefone do cliente de teste onde aparecerem. Conferir quadro a quadro: o layout pode variar.
3. Cortes aprovados (seção 6), clipes 1–3 inseridos depois da parte do "agendamento criado" e **antes** de "bom, a tecnologia agora…". Para o final (stack, testes, conclusão), manter a voz e a webcam originais e cobrir a tela com o clipe 4.
4. Áudio: `highpass=f=80`, redução leve de ruído, `loudnorm` em duas passagens (alvo −16 LUFS, pico real −1,5 dB), fades de ~0,15 s nas emendas.
5. Exportar: `libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 30`, `aac -b:a 192k -ar 48000`, `-t 300`.
6. Homologar: `ffprobe` (duração 300,000 e 9000 quadros), `volumedetect`, inspeção visual de cada emenda, conferir que conflito, remarcação e cancelamento aparecem, e privacidade (sem barra do navegador, e-mail, telefone). Escrever `docs/video/RELATORIO-CORTES.md` (sem dados pessoais).
7. **Transcrição local (opcional):** nenhum modelo de fala vem instalado. Se precisar, crie um `venv` fora do repositório, instale `faster-whisper` e alimente o modelo com o áudio decodificado pelo FFmpeg em vetor NumPy (a versão do PyAV na época falhava ao abrir arquivos). **Não versione a transcrição** (`docs/video/transcricao-original.md` é ignorada pelo Git).
8. Apresentar o MP4 e o relatório ao autor **antes** de pedir autorização para publicar qualquer documento.

## 14. Laudos dos avaliadores (25% da nota)
Os 5 laudos (`docs/laudos/laudo-avaliador-1..5.md` e os PDFs em branco em `docs/laudos/pdf/`) estão com o bloco técnico preenchido e **todos os campos humanos em branco**, status PENDENTE. **0 de 5 avaliações recebidas.** Falta recrutar 5 pessoas reais com consentimento e receber os formulários **preenchidos por elas**. Não inventar avaliadores, notas, datas, assinaturas nem opiniões. O relatório `docs/laudos/RELATORIO-CONSOLIDADO.md` só pode declarar a etapa C concluída com 5 avaliações reais. O PDF acadêmico final só depois dessa coleta.

## 15. Segurança e privacidade
- Nunca versionar: `*.db` e backups, `.env`, credenciais, `*.mp4`/`*.mov`/`*.wav`, `docs/video/clipes/`, `docs/video/transcricao-original.md`, `.venv`, `node_modules`, caches. `.gitignore` já cobre isso.
- Não expor e-mail, telefone, abas, favoritos ou nomes pessoais de terceiros. Não incluir os dados do vídeo original em commits.
- Não executar `git reset --hard` nem `git push --force`; não commitar nem dar push sem autorização expressa do autor; não alterar código do produto sem necessidade.
- Dados do sistema: somente fictícios.

---

## PRÓXIMA MISSÃO (copie e cole em uma nova sessão)
```
Leia docs/video/HANDOFF-OUTRO-COMPUTADOR.md, docs/video/PLANO-REVISAO-VIDEO.md e docs/video/ROTEIRO-CAPTURA.md.
Contexto: AgendaPro, vídeo revisado de EXATOS 300,000 s ainda não produzido; 4 clipes complementares ainda não gravados.
1. Preparar o ambiente (seções 8 e 9 do handoff) com um banco descartável fictício. Não modifique código do produto.
2. Rodar docs/video/preparar-cenarios.ps1 e validar conflito, remarcação e cancelamento pela API real. Reportar as datas obtidas.
3. Orientar o autor a gravar os 4 clipes (ROTEIRO-CAPTURA.md). O autor grava a PRÓPRIA voz: não gerar narração, não simular telas ou respostas.
4. Quando os 4 MP4 estiverem em docs/video/clipes/, montar o vídeo final de 300,000 s (seção 13), com privacidade, cortes aprovados e áudio normalizado.
5. Apresentar o MP4 e o relatório de validação. Não fazer commit nem push sem autorização expressa.
Restrições: sem git reset --hard, sem push --force, sem versionar mídia, banco, .env ou transcrição.
```
