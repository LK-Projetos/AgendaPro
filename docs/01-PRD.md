# PRD — AgendaPro: Sistema Inteligente de Agendamentos

Disciplina: Projeto Integrador Transdisciplinar em Engenharia de Software II
Versão: 0.1 (planejamento) · Status: **para revisão**

## 1. Contexto e problema
Pequenos empreendedores (salões, clínicas, consultorias, estúdios) controlam agenda por papel, planilha ou mensagens. Isso gera conflitos de horário, esquecimentos e retrabalho. O AgendaPro centraliza o cadastro de clientes, serviços e profissionais e oferece uma página pública para reserva sem conflitos.

> O termo "Inteligente" no título é atendido no MVP apenas por **regras automáticas** (validação de conflito, cálculo de horários livres, indicadores). Nenhuma IA é implementada (fora de escopo).

## 2. Objetivos
| ID | Objetivo | Medida de sucesso (a ser coletada de forma real) |
|----|----------|--------------------------------------------------|
| O1 | Eliminar conflitos de horário por profissional | 0 agendamentos sobrepostos aceitos pela API (verificado por testes automatizados) |
| O2 | Permitir reserva pública sem login | Fluxo completo executado nos testes E2E |
| O3 | Dar visão gerencial ao administrador | Dashboard exibe indicadores corretos frente à base de teste |
| O4 | Demonstrar engenharia de software completa | Entregáveis acadêmicos concluídos (seção 9) |
| O5 | Validar com usuários reais | 5 laudos preenchidos por avaliadores reais |

## 3. Personas
- **Administrador/Empreendedor** — gerencia tudo no painel autenticado.
- **Cliente final** — reserva horário na página pública, sem conta.
- **Profissional** — no MVP é apenas um cadastro (sem login próprio).

## 4. Escopo
### Dentro do MVP
RF01 a RF10 (seção 5).
### Fora do MVP (proibido)
Pagamentos, IA, WhatsApp/SMS/e-mail automáticos, assinaturas/planos, integrações externas (Google Calendar etc.), multi-empresa (multi-tenant), login de profissional/cliente, app mobile nativo.

## 5. Requisitos funcionais
| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF01 | Autenticação administrativa (login/logout, rotas protegidas por token) | Alta |
| RF02 | Dashboard com indicadores: agendamentos de hoje, próximos 7 dias, por status, taxa de cancelamento, serviço mais agendado | Média |
| RF03 | CRUD de clientes (nome, e-mail, telefone, observações) com busca | Alta |
| RF04 | CRUD de serviços (nome, descrição, duração, preço de referência, ativo) | Alta |
| RF05 | Cadastro de profissionais e vínculo com os serviços que executam | Alta |
| RF06 | Definição de disponibilidade semanal por profissional (dia, início, fim) | Alta |
| RF07 | Criar, confirmar, remarcar e cancelar agendamentos no painel | Alta |
| RF08 | Página pública de reserva: escolher serviço → profissional → data/horário livre → dados → protocolo | Alta |
| RF09 | Validação de conflitos de horário em toda criação/remarcação | Alta |
| RF10 | Layout responsivo (mobile ≥ 360 px, tablet, desktop) | Média |

## 6. Requisitos não funcionais
| ID | Requisito |
|----|-----------|
| RNF01 | Senhas com hash (bcrypt/argon2); nunca em texto puro nem em log |
| RNF02 | Token JWT com expiração; rotas administrativas retornam 401 sem token |
| RNF03 | Validação de entrada no back (Pydantic) e no front |
| RNF04 | Arquitetura em camadas (rotas → serviços → repositórios → modelos) |
| RNF05 | Cobertura mínima alvo de 70% nos serviços do back-end (meta, a medir de verdade) |
| RNF06 | Horários armazenados em UTC e exibidos em America/Sao_Paulo (ver risco R06) |
| RNF07 | Respostas de erro padronizadas `{code, message, details}` |
| RNF08 | Somente dados fictícios em seed e testes; sem dados pessoais reais |
| RNF09 | Acessibilidade básica: labels, foco visível, contraste AA |

## 7. Critérios de aceite (Gherkin resumido)
- **CA01 (RF01)** Dado um admin válido, quando faz login, então recebe token e acessa o dashboard; com senha inválida recebe 401 e mensagem genérica.
- **CA02 (RF03)** Dado um cliente cadastrado, quando é excluído sem agendamentos, então some da listagem; com agendamentos futuros a API retorna 409.
- **CA03 (RF04)** Dado um serviço com duração 45 min, quando criado, então aparece na página pública apenas se ativo.
- **CA04 (RF05/RF06)** Dado um profissional sem vínculo com um serviço, quando se tenta agendá-lo para esse serviço, então a API retorna 422.
- **CA05 (RF06)** Dadas duas faixas sobrepostas no mesmo dia para o mesmo profissional, quando salvas, então a API recusa (422).
- **CA06 (RF07/RF09)** Dado um agendamento 10:00–10:45 confirmado, quando outro é criado 10:30 para o mesmo profissional, então retorna 409 `SCHEDULE_CONFLICT`.
- **CA07 (RF07)** Dado um agendamento PENDING, quando confirmado, então status = CONFIRMED; confirmar um CANCELLED retorna 409.
- **CA08 (RF07)** Dado um agendamento CONFIRMED, quando remarcado para horário livre, então é atualizado; para horário ocupado retorna 409 e o original permanece.
- **CA09 (RF07)** Dado um agendamento ativo, quando cancelado, então o horário volta a ficar livre.
- **CA10 (RF08)** Dado um visitante, quando conclui a reserva pública, então recebe um protocolo e o agendamento aparece como PENDING no painel.
- **CA11 (RF08)** Dado um horário já reservado, quando o visitante lista horários, então ele não é oferecido; se outra pessoa reservar durante o preenchimento, a confirmação retorna 409 e o front pede novo horário.
- **CA12 (RF02)** Dada uma base de teste conhecida, os indicadores do dashboard coincidem com a contagem esperada.
- **CA13 (RF10)** Em viewport 375×812 não há rolagem horizontal e todos os fluxos principais são concluíveis.

## 8. Premissas
Uma única empresa/estabelecimento; um administrador no seed; fuso fixo America/Sao_Paulo; intervalos de agenda em múltiplos de 15 min.

## 9. Entregáveis acadêmicos
Código (20%), vídeo ~5 min (30%), teste da solução (25%), laudo de qualidade (25%), documentação versionada em Git, modelo de dados documentado, registro de falhas e correções (`docs/13-registro-falhas.md`, criado durante a execução).
