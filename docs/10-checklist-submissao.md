# Checklist de submissão acadêmica

Marque somente o que estiver realmente concluído. Estado em 2026-11-16 (HEAD local `71cfbc3`).

## A. Código e repositório
- [x] Back-end (FastAPI + SQLAlchemy + SQLite): `backend/`
- [x] Front-end (React + TypeScript + Vite): `frontend/`
- [x] README com instalação e execução: [README.md](../README.md)
- [x] Histórico Git local (4 commits); sem `.env`, `.venv`, `node_modules` ou bancos versionados
- [ ] **Publicado no GitHub** `https://github.com/LK-Projetos/AgendaPro.git` — **bloqueado** (ver seção F)
- [ ] Link do repositório conferido (abrir em janela anônima e ver os arquivos)

## B. Documentação (`docs/`)
- [x] [01 Requisitos](01-requisitos.md) · [02 Modelo de dados (classes, DER, dicionário)](02-modelo-dados.md) · [03 API](03-api.md)
- [x] [04 Relatório técnico de testes](04-testes.md) · [05 Manual de uso](05-manual-de-uso.md)
- [x] [06 Roteiro do vídeo](06-roteiro-video.md) · [07 Pendências e falhas](07-pendencias.md)
- [x] [08 Rastreabilidade](08-rastreabilidade.md) · [09 Relatório de entrega](09-relatorio-entrega.md)
- [ ] Nomes dos integrantes e do professor adicionados ao README e ao vídeo
- [ ] Se a disciplina exigir PDF/DOCX, exportar os documentos acima (os diagramas estão em Mermaid; o GitHub os renderiza)

## C. Testes e evidências (`docs/evidencias/`)
- [x] `pytest-saida.txt` (28 passed, cobertura 98%)
- [x] `e2e-saida.txt` (16 passed) · `frontend-build.txt` · `persistencia-reinicio.txt`
- [x] `capturas/` (10 imagens, incluindo agendamento criado, conflito e cancelamento)
- [ ] Se for exigido, reexecutar os testes no dia da entrega e substituir as saídas (comandos no README)

## D. Vídeo (30%)
- [x] Roteiro operacional pronto
- [ ] Banco de demonstração reiniciado imediatamente antes da gravação
- [ ] Vídeo gravado (~5 min, MP4), áudio e legibilidade conferidos
- [ ] Vídeo enviado e **link/arquivo** anexado conforme o AVA/plataforma da disciplina

## E. Laudos de qualidade (25%) — avaliações humanas
Formulários em branco: [laudo-avaliador-1.md](laudos/laudo-avaliador-1.md) · [2](laudos/laudo-avaliador-2.md) · [3](laudos/laudo-avaliador-3.md) · [4](laudos/laudo-avaliador-4.md) · [5](laudos/laudo-avaliador-5.md) · instruções: [INSTRUCOES-AVALIADORES.md](laudos/INSTRUCOES-AVALIADORES.md)
- [ ] 5 pessoas reais recrutadas (anotar o consentimento para citar nomes)
- [ ] 5 laudos preenchidos **pelos próprios avaliadores** (nada preenchido pela equipe)
- [ ] Evidências dos avaliadores em `docs/evidencias/avaliador-N/` (se houver)
- [ ] Falhas relatadas registradas em [07-pendencias.md](07-pendencias.md), corrigidas e retestadas (ou declaradas como pendentes)
- [ ] Resumo dos laudos no relatório e no vídeo

## F. Bloqueio atual: publicação no GitHub
Diagnóstico (consultas somente leitura, sem alterar credenciais):
- `gh auth status`: contas `lktechnologiesbrasil` (ativa) e `LukasAlexandre` (inativa).
- `LK-Projetos` é uma **organização**; o repositório é público e **vazio**. Para a conta ativa, `viewerPermission = READ`.
- `lktechnologiesbrasil` **não é membro** de `LK-Projetos` (não aparece em suas organizações; a consulta de associação retorna 404). Por isso o push é negado (403), com `git` usando o gerenciador de credenciais do Windows nessa conta.
- Não foi testado se `LukasAlexandre` tem escrita, pois isso exigiria trocar de conta.

Caminhos para liberar (decisão sua):
1. Um owner de `LK-Projetos` convida `lktechnologiesbrasil` com papel de escrita (ou o adiciona como colaborador do repositório); após aceitar o convite, o push funciona.
2. Se a conta `LukasAlexandre` for membro com escrita: `gh auth switch --user LukasAlexandre` e depois pedir o push (muda a conta ativa; só faço com sua autorização).
3. Alternativa: criar o repositório em uma conta/organização que você controle e trocar o `origin` (só com sua autorização).
