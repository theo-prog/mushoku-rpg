---
description: Rola dados (ex. /rolar 1d20+3 --cd 15, /rolar teste agilidade --rank espada.deus_da_agua --cd 14)
argument-hint: <expressão ou "teste <atributo>"> [--vantagem|--desvantagem] [--cd N] [--rotulo "..."]
---
Rolagem pedida pelo jogador: `$ARGUMENTS`

1. Rode `python scripts/dados.py $ARGUMENTS` (se não houver `--rotulo`, acrescente um rótulo curto coerente com a cena).
2. Mostre ao jogador a linha do resultado **exatamente como o script imprimiu**, numa linha própria.
3. Se a rolagem foi pedida dentro de uma cena, narre a consequência em 1–3 parágrafos e devolva a palavra ao jogador. Se foi uma rolagem avulsa, não narre nada.

Nunca role "de cabeça" nem altere o resultado.
