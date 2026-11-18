# Checklist de submissão acadêmica

Marque somente o que estiver realmente concluído. Estado em 2026-11-17: código e documentação publicados em `main` (para o commit atual use `git log`); DER corrigido e documentação saneada no lote final; vídeo revisado (300 s) produzido e **aguardando homologação pessoal do autor**. Auditoria: [11-auditoria-academica.md](11-auditoria-academica.md). A entrega acadêmica **não está concluída**: faltam a homologação do vídeo, as **5 avaliações humanas reais (0 de 5)** e a **submissão no AVA**.
Itens marcados **(AVA)** dependem de requisitos que não foram confirmados por mim: conferir no enunciado/AVA antes de enviar. Nada aqui assume exigências que eu não tenha visto.

## 1. Código e GitHub
- [x] Back-end `backend/` e front-end `frontend/`
- [x] README com instalação, execução e testes: [README.md](../README.md)
- [x] **Publicado**: https://github.com/LK-Projetos/AgendaPro (branch `main`, push feito em 2026-11-16)
- [x] Commits de documentação enviados, incluindo a correção do DER e o saneamento final (2026-11-17; ver `git log`)
- [ ] Abrir o link em janela anônima e conferir os arquivos (o repositório é público)
- [ ] (AVA) Confirmar se o repositório deve ser público ou privado e se o professor precisa de convite

## 2. Testes e evidências (`docs/evidencias/`)
- [x] `pytest-saida.txt`: 28 passed, cobertura 98%
- [x] `e2e-saida.txt`: 16 passed · `frontend-build.txt` · `persistencia-reinicio.txt`
- [x] `capturas/`: 10 imagens (dashboard, telas, validação, agendamento criado, conflito, cancelamento, mobile)
- [x] Relatório técnico: [04-testes.md](04-testes.md) · rastreabilidade: [08-rastreabilidade.md](08-rastreabilidade.md)
- [ ] Reexecutar os testes no dia da entrega, se desejado (comandos no README)

## 3. Documentação
- [x] [01 Requisitos](01-requisitos.md) · [02 Modelo de dados: classes, DER, dicionário](02-modelo-dados.md) · [03 API](03-api.md) · [05 Manual](05-manual-de-uso.md) · [07 Pendências](07-pendencias.md) · [09 Relatório de entrega](09-relatorio-entrega.md)
- [x] DER de `02-modelo-dados.md` corrigido (Mermaid exigia um atributo por linha; o `;` causava "Parse error on line 4") e validado com Mermaid 11.17.2 e 10.9.3; atributos, chaves e relacionamentos conferidos contra `models.py`. Diagrama de classes com os métodos reais dos serviços. A renderização no GitHub foi conferida após o push (ver o relatório da entrega)
- [ ] Nomes dos integrantes e do professor no README e no vídeo
- [ ] (AVA) Formato exigido para os documentos (PDF/DOCX/Markdown): hoje estão em Markdown com diagramas Mermaid, que o GitHub renderiza

## 4. Vídeo (30%)
- [x] Roteiro de no máximo 5 min (alvo 4:50): [06-roteiro-video.md](06-roteiro-video.md)
- [x] Ambiente de demonstração com dados fictícios, API e front no ar, 4 telas conferidas
- [ ] Reiniciar o banco de demonstração antes da gravação final (comandos no roteiro)
- [x] Vídeo original gravado pelo autor, 5:00 exatos (arquivo local, não versionado)
- [x] Problemas do original (sem conflito/remarcação/cancelamento, ~88 s de tela parada, áudio baixo, barra do navegador e telefone falado expostos) tratados na versão revisada (ver abaixo)
- [x] Gravações complementares feitas em 2026-11-17 (demonstrações, GitHub e Pytest); as capturas de `02-modelo-dados.md` e `e2e-saida.txt` foram feitas no GitHub com Chrome/Playwright
- [x] Versão revisada exportada (arquivo local, não versionado): 300,000 s, 9000 quadros, H.264/AAC 1280x720 30 fps, −15,9 LUFS. Relatório de cortes: [video/RELATORIO-CORTES.md](video/RELATORIO-CORTES.md)
- [ ] **Homologação do autor**: assistir ao vídeo inteiro (emendas em 0:30, 1:37 e 2:59), conferir narração, privacidade e legibilidade. Não houve revisão humana do áudio; a transcrição automática não é confiável
- [ ] Decidir sobre falas incorretas no original ("Flash API" em vez de FastAPI, "Playwriter", "credo/crudzão"): só regravando
- Continuidade em outro computador: [video/HANDOFF-OUTRO-COMPUTADOR.md](video/HANDOFF-OUTRO-COMPUTADOR.md)
- [ ] (AVA) Formato, tamanho e forma de envio do vídeo (arquivo ou link)

## 5. Laudos de qualidade (25%): cinco avaliações humanas reais
Formulários **em branco**, prontos para os avaliadores:
| Avaliador | PDF preenchível | Markdown |
|---|---|---|
| 1 | [formulario-avaliador-1.pdf](laudos/pdf/formulario-avaliador-1.pdf) | [laudo-avaliador-1.md](laudos/laudo-avaliador-1.md) |
| 2 | [formulario-avaliador-2.pdf](laudos/pdf/formulario-avaliador-2.pdf) | [laudo-avaliador-2.md](laudos/laudo-avaliador-2.md) |
| 3 | [formulario-avaliador-3.pdf](laudos/pdf/formulario-avaliador-3.pdf) | [laudo-avaliador-3.md](laudos/laudo-avaliador-3.md) |
| 4 | [formulario-avaliador-4.pdf](laudos/pdf/formulario-avaliador-4.pdf) | [laudo-avaliador-4.md](laudos/laudo-avaliador-4.md) |
| 5 | [formulario-avaliador-5.pdf](laudos/pdf/formulario-avaliador-5.pdf) | [laudo-avaliador-5.md](laudos/laudo-avaliador-5.md) |

Instruções aos avaliadores: [INSTRUCOES-AVALIADORES.md](laudos/INSTRUCOES-AVALIADORES.md) · Modelo do laudo consolidado (em branco, aguardando dados reais): [laudo-consolidado-MODELO.pdf](laudos/pdf/laudo-consolidado-MODELO.pdf)

- [ ] 5 pessoas reais recrutadas e com consentimento anotado
- [ ] 5 formulários recebidos, preenchidos pelos próprios avaliadores (recebidos: 0 de 5)
- [ ] Falhas relatadas registradas em [07-pendencias.md](07-pendencias.md), corrigidas e retestadas, ou declaradas pendentes
- [ ] Laudo consolidado preenchido **somente** com os dados reais recebidos
- [ ] (AVA) Campos obrigatórios da faculdade: os formulários têm um campo livre "Outros dados exigidos pela instituição"; se o AVA listar campos específicos, incluí-los antes de distribuir

**Os laudos não podem ser declarados concluídos antes de 5 avaliações humanas reais.**

## 6. Pendências reais
1. Homologar o vídeo revisado (300 s) e decidir sobre falas incorretas.
2. Obter as 5 avaliações humanas e consolidar (0 de 5 recebidas).
3. Informar nomes da equipe/professor.
4. Submissão no AVA: confirmar formato, tamanho e campos exigidos (código, vídeo e laudos).
5. (Concluído) Contradições de documentação listadas em [11-auditoria-academica.md](11-auditoria-academica.md) corrigidas no lote final.
6. Limitações técnicas conhecidas: ver [07-pendencias.md](07-pendencias.md) (L01–L08).
