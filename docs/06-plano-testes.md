# Plano de testes

Princípio: **nenhum resultado de teste é registrado antes de ser executado de verdade.** Este documento define o que será testado; resultados ficam em `docs/evidencias/` quando existirem. Execução final de CI: apenas com autorização (ver seção 7).

## 1. Estratégia
| Nível | Ferramenta | Escopo | Meta |
|-------|-----------|--------|------|
| Unitário | Pytest | Services e utilitários puros (conflito, slots, transições, segurança) com repositórios reais em SQLite em memória | ≥ 70% de cobertura nos `services` (meta a medir) |
| Integração | Pytest + FastAPI TestClient | Rotas + banco SQLite temporário, auth, códigos HTTP, schemas | Todos os endpoints cobertos em caso feliz e erro principal |
| E2E | Playwright | Fluxos reais no navegador contra back+front locais com seed fictício | Fluxos críticos (seção 4) |
| Manual | Cinco avaliadores reais | Laudos (docs/07-laudos) | 5 laudos preenchidos |

## 2. Testes unitários (Pytest)
| ID | Alvo | Caso | RF/RN |
|----|------|------|-------|
| U01 | conflito | Sobreposição parcial início/fim/contenção → conflito | RN01 |
| U02 | conflito | Adjacentes (fim = início) → sem conflito | RN01 |
| U03 | conflito | Agendamento CANCELLED não bloqueia | RN01 |
| U04 | disponibilidade | Intervalo fora da faixa → erro; dentro → ok | RN02 |
| U05 | disponibilidade | Faixas sobrepostas rejeitadas | RN13 |
| U06 | serviço×profissional | Profissional sem vínculo → erro | RN03 |
| U07 | fim do agendamento | end = start + duração | RN04 |
| U08 | antecedência | Passado e dentro da antecedência mínima | RN05 |
| U09 | transições | Todas as válidas e inválidas de RN07 | RN07 |
| U10 | remarcação | Ignora o próprio agendamento; falha não altera | RN08 |
| U11 | slots | Dia sem faixa → vazio; slots ocupados removidos | RN12 |
| U12 | segurança | Hash ≠ senha; verificação; JWT expirado inválido | RNF01/02 |
| U13 | dashboard | Contagens por status e taxa de cancelamento (divisão por zero) | RF02 |
| U14 | cliente público | Reutiliza cliente existente por e-mail | RN09 |

## 3. Testes de integração
| ID | Cenário | Esperado |
|----|---------|----------|
| I01 | Login válido/ inválido | 200 com token / 401 |
| I02 | Rota 🔒 sem token / token inválido | 401 |
| I03 | CRUD clientes completo | 201/200/204; e-mail duplicado 409 |
| I04 | Excluir cliente com agendamento futuro | 409 |
| I05 | CRUD serviços; excluir com histórico desativa | 204 e `active=false` |
| I06 | Vincular serviços e definir disponibilidade; sobreposição | 200 / 422 |
| I07 | Criar agendamento válido | 201 PENDING |
| I08 | Criar em conflito | 409 `SCHEDULE_CONFLICT` |
| I09 | Confirmar → remarcar → cancelar | Estados corretos; horário liberado após cancelar |
| I10 | Remarcar para horário ocupado | 409 e original intacto |
| I11 | `/public/slots` reflete reservas | Horário reservado some |
| I12 | `POST /public/appointments` + consulta por protocolo | 201; consulta sem PII |
| I13 | Duas reservas simultâneas do mesmo horário (threads) | Exatamente uma 201, outra 409 |
| I14 | `/dashboard/summary` com seed conhecido | Valores esperados |
| I15 | Validação: payload inválido | 422 com formato de erro padrão |

## 4. Testes E2E (Playwright)
| ID | Fluxo | Verificações |
|----|-------|--------------|
| E01 | Login admin e logout | Redireciona; rota protegida bloqueada sem login |
| E02 | Cadastrar cliente, editar, excluir | Listagem atualiza |
| E03 | Cadastrar serviço e profissional, vincular, definir disponibilidade | Persistem após recarregar |
| E04 | Criar agendamento no painel | Aparece na lista |
| E05 | Conflito no painel | Mensagem de erro clara; nada criado |
| E06 | Confirmar, remarcar, cancelar | Status visual correto |
| E07 | Reserva pública completa | Protocolo exibido; aparece PENDING no painel |
| E08 | Horário ocupado não é oferecido na página pública | Slot ausente |
| E09 | Responsividade 375×812 e 1280×800 | Sem rolagem horizontal; fluxos concluíveis |
| E10 | Dashboard reflete ações | Contadores mudam |

## 5. Dados e ambiente de teste
Banco SQLite temporário por teste/sessão, seed fictício determinístico, relógio controlável (injeção de `now`) para RN05. Testes independentes entre si.

## 6. Registro de falhas e correções
Cada falha (automática ou relatada em laudo) vira uma linha em `docs/13-registro-falhas.md`: ID, origem, descrição, severidade, passos, correção (commit), reteste. Será criado na execução; **somente falhas reais** entram.

## 7. Execução de CI (planejada, não executada)
Arquivo `.github/workflows/ci.yml` será escrito na etapa final com jobs: `backend` (pytest + cobertura), `frontend` (lint, tsc, build), `e2e` (Playwright). **Não será executado, nem enviado ao GitHub, sem autorização explícita.** Durante o desenvolvimento, testes rodam apenas localmente, por demanda.

## 8. Critérios de saída
Todos os casos acima implementados; testes executados com saída real arquivada; falhas críticas/altas corrigidas e retestadas; 5 laudos preenchidos por avaliadores reais.
