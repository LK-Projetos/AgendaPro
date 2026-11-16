# Roteiro de vídeo (~5 min)

Gravar com a aplicação real e o seed fictício. Mostrar apenas resultados reais; não editar saídas de teste.

| Tempo | Cena | Imagem | Narração |
|---|---|---|---|
| 0:00–0:25 | Abertura | Título, integrantes, disciplina | Apresentação do AgendaPro e do objetivo. |
| 0:25–0:55 | Problema e escopo | Slide curto | Agenda manual gera conflitos; MVP: 1 profissional, sem pagamentos/IA/integrações. |
| 0:55–1:40 | Arquitetura | README e árvore de pastas; camadas rotas → serviços → repositórios → modelos | Stack e responsabilidade de cada camada. |
| 1:40–2:15 | Modelo de dados | Diagrama de classes e DER (docs/02) | 3 entidades, relacionamentos, restrições. |
| 2:15–3:50 | Demonstração | Dashboard → cliente (validação de formulário) → serviço → novo agendamento → **conflito rejeitado** → remarcar → cancelar → visão no celular | Mostrar regra de conflito e persistência (reiniciar a API e recarregar). |
| 3:50–4:30 | Testes | Terminal executando `pytest --cov` ao vivo; build do front | Resultado real exibido na tela, o que cobre e o que não cobre (docs/04). |
| 4:30–4:50 | Validação humana | Laudos preenchidos pelos 5 avaliadores (se já existirem) | Resumo honesto; se ainda não houver, dizer que está pendente. |
| 4:50–5:10 | Encerramento | Repositório | Limitações (docs/07) e próximos passos. |

Checklist: ambiente limpo; sem dados reais na tela; resolução 1080p; duração 4:30–5:30; citar nomes de avaliadores apenas com autorização.
