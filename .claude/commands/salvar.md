---
description: Salva a campanha (atualiza campanha/, valida, faz backup e escreve no diário)
argument-hint: [rótulo opcional]
---
Fluxo obrigatório de /salvar (rótulo: `$ARGUMENTS`):

1. **Atualize `campanha/`** com tudo que mudou desde o último registro: personagem (PV, mana, ferimentos, magias, relações, dinheiro, sonhos_registrados), inventário, party, NPCs (atitude, local, status, conhecido_pelo_jogador), facções (atitude, poder), quests e estado (data, local, clima, flags). Use `python scripts/editar.py ...` ou edite o JSON com cuidado.
2. Se algum arco mudou de fase, atualize `historia/arcos.json` (`fase_atual`, `status`, `pistas[].encontrada`). Se uma revelação foi feita, marque `revelada` em `historia/segredos.json` **sem imprimir o arquivo**.
3. Rode `python scripts/validar.py`. Se falhar, corrija e rode de novo até passar.
4. Acrescente ao final de `campanha/diario.md` uma entrada:
   `## Sessão N — <data do mundo legível> — <título da cena>` seguida de 3–8 linhas: o que aconteceu, decisões do jogador, consequências e pontas soltas. Nunca apague entradas antigas. Incremente `estado.sessao` se for fim de sessão.
5. Rode `python scripts/backup.py --nome "<rótulo>"` (sem `--nome` se não houver rótulo).
6. Confirme ao jogador em uma ou duas linhas (nome do backup) e, se a sessão continua, volte à cena.
