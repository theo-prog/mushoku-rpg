---
description: Treinar para subir de rank, aprender magia ou técnica, ou crescer a mana
argument-hint: <o que treinar> [por quanto tempo]
---
Treino pedido: `$ARGUMENTS`

Siga `regras/sistema.md`, seção "Treino e progressão":
1. Determine o que se treina (escola de magia, estilo de espada, magia nova, conjuração silenciosa, capacidade de mana, idioma) e confirme **mentor**, **local**, **tempo** e custo (dinheiro, favores).
2. Verifique os requisitos: subir de rank exige o tempo mínimo da tabela **e** um mentor de rank superior ou um evento marcante. Sem isso, o treino só dá progresso parcial.
3. Avance o tempo com `python scripts/avancar_tempo.py <dias>`. Treinos longos são elipses: narre o que mudou no mundo, nas notícias e nas pessoas próximas.
4. Teste com `python scripts/dados.py teste <atributo> --rank <caminho> --cd <CD da tabela>` e mostre o resultado. Falha não apaga o tempo gasto: registre o progresso parcial em `personagem.notas`.
5. Em sucesso: atualize `ranks`, `magias_conhecidas`, `tecnicas`, `mana_max` ou `encantacao_silenciosa` e rode `python scripts/validar.py`.
6. Narre a cena-chave do treino (o momento em que algo "encaixa"), com o mentor falando com a voz dele.
