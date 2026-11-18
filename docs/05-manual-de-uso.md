# Manual de uso simplificado

1. **Iniciar**: siga o [README](../README.md) (API na porta 8000, interface na 5173) e abra http://127.0.0.1:5173.
2. **Dashboard**: mostra agendamentos de hoje, próximos 7 dias, ativos, cancelados, receita prevista e os próximos agendamentos.
3. **Clientes**: "+ Novo cliente" → nome, e-mail, telefone com DDD → Salvar. Use a busca para filtrar. "Editar" e "Excluir" na linha. Cliente com agendamentos não pode ser excluído.
4. **Serviços**: "+ Novo serviço" → nome, descrição (opcional), duração (15 a 480 min, de 15 em 15) e preço. Serviço com agendamentos não pode ser excluído.
5. **Agendar**: aba Agendamentos → "+ Novo agendamento" → cliente, serviço, data e hora → Salvar. O horário de término é calculado pela duração do serviço. O início deve ser em múltiplos de 15 minutos e não pode estar no passado.
6. **Conflito**: se o intervalo se sobrepõe a outro agendamento ativo, aparece "Horário indisponível…" e nada é salvo. Altere o horário e salve novamente.
7. **Remarcar**: botão "Remarcar" na linha → novo horário. Em caso de conflito ou de horário no passado, o agendamento original permanece. Só agendamentos ativos podem ser remarcados.
8. **Cancelar**: botão "Cancelar" → confirmar. O horário volta a ficar livre.
9. **Filtros**: na lista de agendamentos, filtre por status e por dia.
10. **Erros comuns**: campos obrigatórios e formatos inválidos são indicados abaixo de cada campo; se a API estiver parada, a tela mostra "Não foi possível conectar ao servidor" com botão para tentar novamente.
