# Riscos, dependências e pendências

## Riscos
| ID | Risco | Prob. | Impacto | Mitigação |
|----|-------|-------|---------|-----------|
| R01 | Corrida na reserva pública gera duplo agendamento no SQLite | Média | Alto | RN14 (transação com bloqueio) + teste I13 |
| R02 | Prazo curto frente ao escopo (10 RFs + vídeo + 5 laudos) | Alta | Alto | Priorização P0/P1/P2 no backlog; cortar P2 primeiro |
| R03 | Dificuldade de recrutar 5 avaliadores reais | Média | Alto | Convidar cedo; laudo curto; testar em 2 dispositivos; **nunca simular** |
| R04 | Divergência de contrato entre front e back | Média | Médio | OpenAPI como fonte única; MSW; pontos S1–S3 |
| R05 | Instabilidade de testes E2E | Média | Médio | Seed determinístico, esperas por seletor, banco isolado |
| R06 | Erros de fuso horário/horário de verão | Média | Alto | UTC no banco, conversão na borda, testes com datas de borda |
| R07 | Vazamento de dados pessoais em repositório/vídeo | Baixa | Alto | Só dados fictícios; `.env` ignorado; revisão antes de gravar |
| R08 | Ambiente do avaliador impede execução local | Média | Médio | Roteiro de instalação simples; opção de sessão guiada presencial/remota |
| R09 | Conflito de arquivos entre agentes | Baixa | Médio | Diretórios isolados (doc 09) |
| R10 | Dependências indisponíveis/incompatíveis (Node, Python) | Baixa | Médio | Fixar versões; documentar no README |

## Dependências
- Python 3.11+, Node 20+, npm.
- Bibliotecas: fastapi, uvicorn, sqlalchemy, alembic, pydantic, passlib/bcrypt (ou argon2), python-jose/pyjwt, pytest, pytest-cov, httpx; react, react-router, @tanstack/react-query, typescript, vite, playwright (browsers instalados).
- Repositório remoto GitHub `LK-Projetos/AgendaPro` (hoje vazio) — push só com autorização.
- Cinco avaliadores reais, com disponibilidade e consentimento.
- Ferramenta de gravação de vídeo/áudio.

## Requisitos e decisões pendentes (precisam de resposta do usuário)
| ID | Pendência | Sugestão padrão |
|----|-----------|-----------------|
| P01 | Cliente final pode cancelar/remarcar pelo protocolo? | Não no MVP |
| P02 | Bloqueios pontuais (folgas, feriados) por profissional? | Fora do MVP |
| P03 | Antecedência mínima de reserva pública | 60 min |
| P04 | Reserva pública nasce PENDING ou CONFIRMED? | PENDING (admin confirma) |
| P05 | Um profissional pode atender vários clientes simultaneamente? | Não (1 por vez) |
| P06 | Formato de entrega do vídeo, limites e plataforma | A definir pela disciplina |
| P07 | Entrega dos diagramas: Mermaid basta ou exigem ferramenta específica (StarUML, draw.io)? | Mermaid + export PNG |
| P08 | Nomes dos integrantes/equipe e do professor para o vídeo e README | A informar |
| P09 | Licença e visibilidade do repositório | Privado, sem licença |
| P10 | Hospedagem para demonstração (local vs. deploy) | Local; deploy só com autorização |
| P11 | Idioma da interface | pt-BR |
