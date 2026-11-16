# Requisitos

Escopo: um estabelecimento, um profissional, sem autenticação, pagamentos, notificações, IA ou integrações.

## Requisitos funcionais
| ID | Requisito | Onde |
|----|-----------|------|
| RF01 | Dashboard com indicadores calculados do banco: agendamentos hoje, próximos 7 dias, ativos, cancelados (e %), receita prevista, total de clientes e serviços, próximos 5 agendamentos | `GET /api/dashboard`, aba Dashboard |
| RF02 | CRUD de clientes (nome, e-mail, telefone) com busca por nome/e-mail | `/api/clients`, aba Clientes |
| RF03 | CRUD de serviços (nome, descrição, duração, preço) | `/api/services`, aba Serviços |
| RF04 | CRUD de agendamentos (criar, listar com filtros, editar, excluir) | `/api/appointments`, aba Agendamentos |
| RF05 | Remarcar e cancelar agendamentos | `POST /appointments/{id}/reschedule` e `/cancel` |
| RF06 | Bloquear agendamentos conflitantes | RN01 |
| RF07 | Validar formulários (front e back) | schemas Pydantic + validação no front |
| RF08 | Persistir no SQLite | `backend/agendapro.db` |
| RF09 | Tratar erros com mensagens claras | formato `{code,message,details}` e avisos na tela |
| RF10 | Dados fictícios de demonstração | `python -m app.seed` |

## Requisitos não funcionais
| ID | Requisito |
|----|-----------|
| RNF01 | Arquitetura em camadas: rotas → serviços (regras) → repositórios → modelos |
| RNF02 | Layout responsivo (tabelas viram cartões abaixo de 680 px) |
| RNF03 | Sem dependência de mock em fluxos críticos; front consome a API real |
| RNF04 | Somente dados fictícios |
| RNF05 | Chaves estrangeiras e restrições CHECK ativas no SQLite |

## Regras de negócio
| ID | Regra |
|----|-------|
| RN01 | **Conflito**: dois agendamentos com status `SCHEDULED` conflitam se `início_A < fim_B` e `fim_A > início_B`. Horários encostados (fim = início) são permitidos. Cancelados não bloqueiam. Resposta 409 `SCHEDULE_CONFLICT`. |
| RN02 | Fim = início + duração do serviço, calculado na criação/edição. |
| RN03 | Não é permitido agendar/remarcar para o passado (422). |
| RN04 | Início em múltiplos de 15 minutos; duração do serviço 15–480 min em múltiplos de 15. |
| RN05 | Remarcar/editar ignora o próprio agendamento na checagem de conflito; em caso de erro nada é alterado. |
| RN06 | Só agendamentos `SCHEDULED` podem ser remarcados/editados; cancelar duas vezes retorna 409. |
| RN07 | Cliente com agendamentos (qualquer status) ou serviço com agendamentos não pode ser excluído (409). Excluir o agendamento remove o registro. |
| RN08 | E-mail de cliente e nome de serviço (sem diferenciar maiúsculas) são únicos. |
| RN09 | Telefone normalizado para 10–11 dígitos; e-mail normalizado em minúsculas. |
| RN10 | Horários são locais do estabelecimento (sem fuso). |

## Escolhas de escopo
- Status: apenas `SCHEDULED` e `CANCELLED` (sem "concluído"; não pedido).
- Não há horário de funcionamento nem folgas (fora do escopo); o bloqueio é só por sobreposição.
