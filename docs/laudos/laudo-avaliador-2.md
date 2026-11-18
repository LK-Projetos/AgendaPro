# Laudo de Avaliação — Avaliador 2 de 5

> Preencher **somente** com observações reais de uma pessoa real que usou o sistema. Não preencher por simulação. Não registrar dados pessoais sensíveis; usar dados fictícios no teste.

| Campo | Valor |
|-------|-------|
| Nome do avaliador | |
| Perfil (ex.: empreendedor, estudante, outro) | |
| Data da avaliação | ____/____/______ |
| Autoriza citar o nome no vídeo/relatório? | ( ) Sim ( ) Não |
| Versão/commit testado | |
| Dispositivo e navegador | |
| Duração aproximada | |

## 0. Dados técnicos (preenchidos pela equipe — não são opinião do avaliador)
| Item | Informação |
|------|-----------|
| Projeto | AgendaPro — Sistema de Agendamentos (MVP acadêmico) |
| Disciplina | Projeto Integrador Transdisciplinar em Engenharia de Software II — Cruzeiro do Sul Virtual |
| Versão disponibilizada para teste | Código em `b4252fb` (2026-11-16); os commits posteriores em `main` alteram apenas documentação, não `backend/` nem `frontend/` (informar o commit testado no campo acima) |
| Repositório | https://github.com/LK-Projetos/AgendaPro |
| Status deste laudo | **PENDENTE — nenhuma avaliação humana registrada** |

**Funcionalidades disponíveis:** dashboard; CRUD de clientes (busca, e-mail único); CRUD de serviços (duração 15–480 min, preço); criar, editar, remarcar, cancelar e excluir agendamentos; bloqueio de conflito de horário; validação de formulários; layout responsivo. Não há login, pagamentos, notificações nem fuso horário (ver `docs/07-pendencias.md`).

**Critérios de avaliação:** correção funcional, clareza das mensagens, usabilidade, aparência/layout, desempenho percebido e confiança na agenda (notas 1 a 5 na seção 6).

**Como executar o teste:** subir API (porta 8000) e interface (porta 5173) conforme o `README.md` e seguir o roteiro de 9 passos em `docs/laudos/INSTRUCOES-AVALIADORES.md`.

**Referências técnicas comprovadas (testes automatizados, não substituem este laudo):** Pytest 28 aprovados, cobertura 98% (`docs/evidencias/pytest-saida.txt`); E2E Playwright 16 aprovados em duas execuções (`docs/evidencias/e2e-saida.txt`); persistência após reinício (`docs/evidencias/persistencia-reinicio.txt`); capturas em `docs/evidencias/capturas/`.

**Limitações conhecidas que o avaliador pode encontrar:** L01–L08 em `docs/07-pendencias.md` (ex.: agenda aceita madrugada; sem paginação).

## 1. Funcionalidades testadas
Marque e descreva o resultado de cada uma.

| Funcionalidade | Testou? | Resultado (Sucesso / Falha / Parcial) | Comentário |
|----------------|---------|----------------------------------------|-----------|
| Dashboard com indicadores | ( ) | | |
| CRUD de clientes (criar, editar, excluir, buscar) | ( ) | | |
| CRUD de serviços (preço e duração) | ( ) | | |
| Criar agendamento | ( ) | | |
| Editar agendamento | ( ) | | |
| Remarcar agendamento | ( ) | | |
| Cancelar agendamento | ( ) | | |
| Bloqueio de horário conflitante | ( ) | | |
| Validação de formulários e mensagens de erro | ( ) | | |
| Layout no celular | ( ) | | |

## 2. Funcionou com sucesso
-

## 3. Falhas encontradas
| # | Onde | Passos para reproduzir | Esperado | Obtido | Gravidade (Baixa/Média/Alta/Crítica) |
|---|------|------------------------|----------|--------|--------------------------------------|
| 1 | | | | | |

## 4. Não testado (e motivo)
-

## 5. Sugestões de melhoria
-

## 6. Avaliação de qualidade (nota de 1 a 5, 5 = excelente)
| Critério | Nota |
|----------|------|
| Facilidade de uso | |
| Clareza das mensagens | |
| Aparência/layout | |
| Desempenho percebido | |
| Confiança nos resultados (agenda correta) | |

## 7. Evidências
Listar arquivos em `docs/evidencias/avaliador-2/` (capturas de tela, gravações, anotações), com legenda.

| Arquivo | Descrição |
|---------|-----------|
| | |

## 8. Registro de tratamento (preenchido pela equipe depois)
| Falha # | ID no registro de falhas | Correção (commit) | Reteste |
|---------|--------------------------|-------------------|---------|
| | | | |

Identificação de aceite do avaliador (nome ou rubrica, a ser feita pelo próprio avaliador): ______________________
Data do aceite: ____/____/______

> Campos das seções 1 a 7 e o aceite devem ser preenchidos exclusivamente pelo avaliador. A seção 8 é preenchida pela equipe após o recebimento.
