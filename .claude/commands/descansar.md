---
description: Descansar (curto, uma noite ou vários dias)
argument-hint: <curto | noite | N dias>
---
Descanso pedido: `$ARGUMENTS`

1. **Curto** (1 hora): recupera mana igual a 1 + Intelecto (mínimo 1) e permite um teste de Vigor CD 10 para recuperar 1d4 PV. Atualize com `python scripts/editar.py personagem add mana N` etc. Não avance a data.
2. **Noite** ou **N dias**: rode `python scripts/avancar_tempo.py <N> --descanso` (noite = 1). O script recupera mana e PV, dispara eventos dos relógios e lembra de narrar os sonhos.
3. **Antes de dormir**, pergunte (se não estiver claro) **onde** e **com quem** o personagem dorme e se alguém vigia. Isso importa; não explique por quê.
4. Ao acordar: se o personagem sonha, narre o sonho (consulte `historia/segredos.json` em silêncio para decidir se alguma das vozes aparece) e registre em `sonhos_registrados`. Se é Sem-Sonho, narre a ausência e como os outros reagem a ela.
5. Ferimentos persistentes não somem com descanso, só com cura de rank suficiente ou o tempo indicado.
6. Narre o que mudou no mundo durante o descanso (notícias, viajantes, clima) se o script disparou eventos que o personagem ouviria.
