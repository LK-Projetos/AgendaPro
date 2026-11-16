# Instruções para os 5 avaliadores

Obrigado por avaliar o AgendaPro. Leva cerca de 15 a 20 minutos. O sistema usa **apenas dados fictícios**: não digite dados pessoais reais.

## Como abrir o sistema
Quem aplica o teste deixa a aplicação rodando (veja o README: API na porta 8000 e interface na 5173) e abre http://127.0.0.1:5173. Se o sistema estiver em outro computador, use o endereço informado pela equipe.

## Roteiro (marque o resultado no laudo)
1. **Dashboard**: abra e confira se os números e a lista de próximos agendamentos fazem sentido.
2. **Clientes**: cadastre um cliente fictício; tente salvar com campos vazios e com e-mail inválido; edite o cliente; tente cadastrar outro com o mesmo e-mail.
3. **Serviços**: cadastre um serviço com duração 45 e preço `90,50`; tente duração 50 e preço `abc`; edite o preço.
4. **Agendar**: crie um agendamento para amanhã às 10:00 e veja o horário de término.
5. **Conflito**: tente criar outro para as 10:15 do mesmo dia. O sistema deve recusar com uma mensagem.
6. **Remarcar**: remarque o agendamento para outro horário livre; depois tente remarcar para um horário ocupado.
7. **Cancelar**: cancele um agendamento e confirme que ele aparece como cancelado.
8. **Excluir**: tente excluir um cliente que tem agendamentos (deve ser bloqueado).
9. **Celular**: abra no celular (ou reduza a janela) e repita o passo 4.

## Preenchimento
Use uma cópia do seu laudo (`laudo-avaliador-N.md`) com **suas observações reais**: o que funcionou, falhas (com passos para reproduzir), o que não testou e sugestões. Anexe capturas em `docs/evidencias/avaliador-N/`, se houver. A equipe não deve preencher o laudo no lugar do avaliador.
