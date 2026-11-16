# Validação manual em navegador (2026-11-16)
n> **Nota:** validação manual feita antes do E2E. Os itens 13 (serviço) e a dependência de `window.confirm` substituído foram refeitos e confirmados no Playwright (ver [04-testes.md](../04-testes.md), H01 e H03).

Quem executou: Claude, no navegador embutido do aplicativo, contra `http://127.0.0.1:5173` (Vite em modo dev) → API `http://127.0.0.1:8000` → `backend/agendapro.db` com seed fictício. Dados de "hoje" do seed são relativos à data da execução (2026-11-16).

| # | Fluxo | Resultado observado |
|---|---|---|
| 1 | Abrir a aplicação | Dashboard carregou com dados reais: hoje 2, próximos 7 dias 6, ativos 8, cancelados 2 (20%), receita prevista R$ 460,00, 6 clientes, 4 serviços, lista de próximos agendamentos |
| 2 | Criar agendamento às 18:15 (Corte, 30 min) com Diego já agendado 18:00–18:30 | Mensagem "Horário indisponível: já existe um agendamento neste intervalo."; nada criado |
| 3 | Criar o mesmo agendamento às 20:00 | Criado (id 11, 20:00–20:30, SCHEDULED), confirmado via API |
| 4 | Remarcar o id 11 para 19:15 (conflita com Elisa 19:00–19:30) | Erro de conflito exibido no modal; modal permaneceu aberto |
| 5 | Remarcar o id 11 para 21:00 | API: início 21:00, fim 21:30, SCHEDULED |
| 6 | Cancelar o id 11 | API: status CANCELLED; modal fechado |
| 7 | Cliente: salvar formulário vazio | 3 mensagens de validação (nome, e-mail, telefone) |
| 8 | Cliente: e-mail já existente | "Já existe um cliente com este e-mail." |
| 9 | Cliente: cadastrar Gustavo Demo com telefone `(11) 98888-1111` | Listado com telefone formatado |
| 10 | Excluir Gustavo (sem agendamentos) | Removido da lista |
| 11 | Excluir Ana (com agendamentos) | Aviso: "Cliente possui agendamentos. Exclua ou cancele-os antes de remover o cliente." |
| 12 | Serviço: formulário vazio / duração 50 | Mensagens de nome e preço; "Duração: 15 a 480 min, em múltiplos de 15." |
| 13 | Serviço: criar "Hidratação" (45 min, 90,50), editar preço, excluir | A exclusão funcionou (a linha existia na lista). **Minhas verificações automáticas de texto para "criado" e "editado" retornaram falso** (provável diferença de espaço no formato de moeda `R$ 90,50`); a criação e edição foram confirmadas só indiretamente. Não revalidado visualmente |
| 14 | Excluir serviço com agendamentos (Coloração) | Aviso: "Serviço possui agendamentos e não pode ser excluído." |
| 15 | Persistência: parar a API, reiniciar, consultar | 11 agendamentos antes e 11 depois; id 11 continuou CANCELLED |
| 16 | Responsividade 375×812 nas 4 abas | Sem rolagem horizontal (largura do documento = 375) |

Observações do método: para confirmar exclusões, substituí `window.confirm` por uma função que retorna verdadeiro (via console), em vez de clicar no diálogo nativo. Telas não foram capturadas em imagem.
