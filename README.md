# AgendaPro — Sistema de Agendamentos (MVP acadêmico)

Projeto Integrador Transdisciplinar em Engenharia de Software II — Cruzeiro do Sul Virtual.
Aplicação web para um pequeno estabelecimento com **um profissional**: cadastro de clientes e serviços, agenda com bloqueio de conflitos, remarcação, cancelamento e dashboard.

> Ambiente de demonstração acadêmica: sem login, sem pagamentos, sem notificações, sem integrações externas, sem IA. Todos os dados do seed são **fictícios**.

## Stack
React 19 + TypeScript + Vite · Python 3.13 + FastAPI · SQLAlchemy 2 + SQLite · Pytest.

## Pré-requisitos
Python 3.11+ e Node.js 20+ (testado com Python 3.13 e Node 24, Windows 11).

## Instalação e execução (2 terminais)

**Terminal 1 — API (porta 8000)**
```bash
cd backend
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1      Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed            # opcional: dados fictícios (não apaga nada; ignora se já houver dados)
python -m uvicorn app.main:app --port 8000
```
Documentação interativa da API: http://127.0.0.1:8000/docs

**Terminal 2 — Interface (porta 5173)**
```bash
cd frontend
npm install
npm run dev
```
Abra http://127.0.0.1:5173. O Vite encaminha `/api` para a porta 8000.

O banco é o arquivo `backend/agendapro.db` (criado automaticamente, não versionado). Para zerar a demonstração, apague esse arquivo com a API parada e rode o seed novamente.

## Testes
```bash
cd backend
python -m pytest -v --cov=app --cov-report=term-missing   # testes automatizados da API
cd ../frontend
npm run typecheck && npm run lint && npm run build         # verificação estática e build
```
Resultados reais da última execução: [docs/04-testes.md](docs/04-testes.md) e [docs/evidencias/](docs/evidencias/).

## Documentação
| Documento | Conteúdo |
|-----------|----------|
| [01 Requisitos](docs/01-requisitos.md) | Requisitos funcionais, não funcionais, regras de negócio |
| [02 Modelo de dados](docs/02-modelo-dados.md) | Diagrama de classes, DER, dicionário de dados |
| [03 API](docs/03-api.md) | Endpoints REST e formato de erros |
| [04 Testes](docs/04-testes.md) | Plano, resultados reais, limitações |
| [05 Manual de uso](docs/05-manual-de-uso.md) | Passo a passo simplificado |
| [06 Roteiro de vídeo](docs/06-roteiro-video.md) | Vídeo de ~5 min |
| [07 Pendências](docs/07-pendencias.md) | Falhas conhecidas e o que falta |
| [Laudos](docs/laudos/) | 5 templates para avaliadores humanos (em branco) |
| [Planejamento inicial](docs/planejamento-inicial/) | Plano anterior, com escopo maior (superado pelo escopo deste MVP) |

## Estrutura
```
backend/app/   routers/api.py (rotas) · services.py (regras) · repositories.py (persistência)
               models.py · schemas.py (validação) · errors.py · database.py · seed.py
backend/tests/ testes Pytest
frontend/src/  App.tsx · pages/ (Dashboard, Clients, Services, Appointments) · api.ts · components.tsx
docs/          documentação, laudos, evidências
```
