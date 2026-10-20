---
description: Carrega a campanha e abre com recap (também é o ritual de início de cada sessão)
argument-hint: [nome de backup opcional]
---
1. Se `$ARGUMENTS` não estiver vazio: rode `python scripts/backup.py --listar`, confirme o nome com o jogador se houver ambiguidade e rode `python scripts/backup.py --restaurar <pasta>`.
2. Rode `python scripts/validar.py` (corrija antes de seguir se falhar).
3. Rode `python scripts/sessao.py resumo`: data, local, PV/mana, party, quests ativas, relógios, notícias, arcos ativos e as **3 últimas entradas do diário**.
4. Leia `campanha/personagem.json`, `campanha/estado.json` e os NPCs do local atual (`python scripts/sessao.py npcs --local <local_atual>`). Em `historia/arcos.json`, só os arcos ativos. Consulte `historia/segredos.json` em silêncio, se precisar, **sem imprimir**.
5. Catálogos (`dados/`) só sob demanda.
6. Se o personagem ainda não existe (`status_criacao: pendente`), conduza a criação de personagem (ver CLAUDE.md).
7. Abra com um **recap curto** ("Anteriormente…", 3–5 linhas, em segunda pessoa, só com o que o personagem sabe) e retome a cena exatamente onde parou, terminando numa situação aberta.
