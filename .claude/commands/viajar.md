---
description: Viajar para outro local (avança o tempo pela rota)
argument-hint: <id ou nome do destino>
---
Destino: `$ARGUMENTS`

1. Rode `python scripts/sessao.py mapa` para ver as rotas a partir do local atual. Sem rota direta, proponha o caminho por etapas (o jogador decide).
2. Confirme com o jogador: meio de transporte, preparativos (comida, dinheiro, guia, escolta) e se quer **viajar em elipse** (resumo) ou jogar os encontros.
3. Para cada etapa: `python scripts/avancar_tempo.py --viagem <destino>`.
4. Encontros: a cada 7 dias de viagem (ou fração), role `python scripts/dados.py 1d10 --rotulo "Encontro na estrada"`. Resultado ≤ perigo da rota = encontro (monstro de `dados/monstros.json` do continente, bandidos, refugiados, Ocos, agentes de facções). Prefira ganchos dos arcos secundários.
5. Narre a viagem como elipse sensorial: paisagem, clima, cansaço, conversas, mudanças na party e as **notícias** que chegam pelo caminho (eventos disparados). Desconte dinheiro e suprimentos.
6. Termine chegando ao destino numa situação aberta.
