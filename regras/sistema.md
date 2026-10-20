# Sistema de jogo

Todas as rolagens usam `python scripts/dados.py` e o resultado é mostrado ao jogador. O Mestre nunca rola "de cabeça".

---

## 1. Atributos

| Atributo | Usado para |
|---|---|
| **Força** (`forca`) | golpes pesados, carregar, quebrar, agarrar |
| **Agilidade** (`agilidade`) | iniciativa, esquiva, armas leves, furtividade, acrobacia |
| **Vigor** (`vigor`) | PV, resistir a dor, veneno, cansaço, manter encantação sob dano |
| **Intelecto** (`intelecto`) | conjurar, estudar, lembrar, deduzir, mana |
| **Percepção** (`percepcao`) | notar, rastrear, ler intenções, mirar à distância |
| **Presença** (`presenca`) | convencer, intimidar, liderar, mentir, encantar plateias |

Os atributos são **modificadores** (de −2 a +4 na criação; máximo absoluto +6 para mortais comuns).
- **Criação**: distribua o conjunto `+3, +2, +1, +1, 0, −1`, depois aplique os modificadores da raça (`dados/racas.json`).
- **Crianças** (até 12 anos): −1 em Força e Vigor (mínimo −2) até completar 13 anos.
- **Maturidade**: aos 15 e aos 20 anos, +1 num atributo à escolha (máx. +4 nesse momento).
- **Eventos marcantes**: o Mestre pode conceder +1 num atributo, no máximo uma vez por Ato.

## 2. Testes

**`1d20 + atributo + bônus de rank (se aplicável) + perícia (+2 se treinada) + modificadores` ≥ CD**

| Bônus de rank | Nenhum | Iniciante | Intermediário | Avançado | Santo | Rei | Imperador | Deus |
|---|---|---|---|---|---|---|---|---|
| | 0 | +1 | +2 | +4 | +6 | +9 | +12 | +15 |

O bônus de rank vale só quando o rank se aplica (magia de fogo usa o rank de fogo; um golpe do estilo Deus da Água usa o rank desse estilo).

| CD | Dificuldade |
|---|---|
| 8 | trivial sob pressão |
| 12 | fácil |
| 15 | médio |
| 18 | difícil |
| 22 | muito difícil |
| 26 | heroico |
| 30 | lendário |

- **Vantagem / desvantagem**: role 2d20 e use o maior / menor (`--vantagem` / `--desvantagem`). Não acumulam; se houver as duas, anulam-se.
- **Resultados** (o script imprime): 20 natural = **crítico**; 1 natural = **falha crítica**; ≥ CD+10 = **excepcional**; ≥ CD = **sucesso**; até 2 abaixo = **parcial** (consegue com custo, ou falha por pouco e ganha algo); abaixo disso = **falha**. A falha sempre acontece e sempre muda a situação.
- **Testes resistidos**: os dois rolam; maior total vence; empate favorece quem defende.
- Exemplo: `python scripts/dados.py teste agilidade --rank espada.deus_da_agua --cd 15`.

### Perícias (não marciais)
Atletismo, Acrobacia, Furtividade, Sobrevivência, Rastreio, Medicina, Investigação, História e Lendas, Arcanismo, Etiqueta, Persuasão, Enganação, Intimidação, Intuição, Cavalgar, Navegação, Ofício (escolha), Idiomas. **4 perícias na criação** (+1 por origem), +1 a cada Ato ou treino de 6 meses.

## 3. Ranks substituem níveis
Não há XP nem níveis. O poder vem de **ranks**: por **escola de magia** (fogo, água, terra, vento, cura, desintoxicação, barreira, invocação) e por **estilo de espada** (Deus da Espada, Deus da Água, Deus do Norte). Subir de rank exige **tempo de treino, mentor ou evento marcante** e um teste (seção 9).

### Hierarquia
- Quem enfrenta alguém **2 ou mais ranks acima** na mesma arena (marcial contra marcial, mágica contra mágica, ou o maior rank de cada um num confronto misto) tem **desvantagem** em ataques e testes resistidos contra ele.
- **3 ou mais ranks acima**: além da desvantagem, só um crítico causa dano real (o resto é arranhão).
- Isso é intencional: rank Avançado não vence rank Rei. Encontros com os Sete Grandes Poderes são para fugir, negociar ou não estar lá.

## 4. Recursos

### Pontos de Vida (PV)
`PV máx = 10 + 3×Vigor + 3×(bônus do maior rank de espada) + bônus racial`. Crianças até 12 anos: `8 + 2×Vigor`.

### Mana
`Mana máx = 10 + 2×Intelecto + reserva de crescimento`.
A **reserva de crescimento** vem do treino (por ano de prática real de magia), multiplicada pela capacidade:

| Idade do treino | Reserva por ano |
|---|---|
| até 10 anos | +5 |
| 11–15 | +3 |
| 16–20 | +1 |
| adulto | +1 a cada 2 anos |

| `capacidade_mana_crescimento` | Multiplicador |
|---|---|
| nenhuma | ×0 |
| baixa | ×0,5 |
| normal | ×1 |
| alta | ×1,5 (talento raro) |
| anomala | ×2, e +15 de reserva inicial (Sem-Sonho com mana anormal) |

- **Esgotamento**: com 0 de mana, desvantagem em tudo por 1 hora; conjurar sem mana suficiente exige teste de Vigor CD 15 e causa 1d6 de dano por ponto faltante.
- **Recuperação**: noite de sono = mana cheia. Descanso curto (1 hora) = 1 + Intelecto.

## 5. Magia

- Ver `dados/magias.json` (`/magias`). Cada magia tem custo, tempo de conjuração, alcance, efeito e dano.
- **Conjurar uma magia do seu rank ou abaixo** não exige teste fora de combate. Em combate:
  - **Ataque mágico contra um alvo**: `1d20 + Intelecto + rank da escola` contra a **Defesa** do alvo.
  - **Área**: os alvos fazem teste de Agilidade (ou Vigor) contra **CD = 10 + Intelecto + rank da escola**; sucesso = metade do dano.
- **Tempo de conjuração**: `ação` (no seu turno), `ação completa` (gasta movimento e ação), `1 turno` (a magia sai no início do seu próximo turno), `2+ turnos`, `ritual` (minutos ou horas).
- **Interrupção**: sofrer dano enquanto encanta uma magia de 1 turno ou mais exige teste de Vigor CD 10 + metade do dano; falha = a magia se perde e metade da mana é gasta.
- **Acima do seu rank**: só um rank acima; teste de Intelecto + rank, CD 15 (+5 se Santo ou acima), custo dobrado; falha = mana perdida e 1d6 de dano por rank da magia (o corpo não aguenta).
- **Encantação abreviada**: magias **dois ranks abaixo** do seu têm o tempo de conjuração reduzido em um passo.
- **Conjuração silenciosa** (traço `encantacao_silenciosa`): em magias com `pode_silenciosa: true`,
  - reduz o tempo de conjuração em um passo (uma `ação` vira **ação rápida**, que pode ser somada a outra ação no mesmo turno, uma vez por rodada);
  - não pode ser interrompida por dano nem silenciada;
  - inimigos não podem "ler" a encantação para reagir;
  - dá **vantagem na iniciativa** e +2 no primeiro ataque mágico de um combate em que o inimigo não sabia que você conjura.
- **Combinadas**: exigem rank Intermediário nas duas escolas envolvidas.
- **Barreiras** bloqueiam magias de rank igual ou inferior ao delas até esgotar seus pontos de absorção.
- **Magia divina** (cura, desintoxicação, barreira) é ensinada pela Igreja; usá-la sem licença em terras de Millis é mal visto (às vezes crime).

## 6. Combate

### Rodada
1. **Iniciativa**: `1d20 + Agilidade` (vantagem com conjuração silenciosa pronta ou emboscada).
2. Cada um, em ordem: **movimento** (~10 m), **1 ação** e, fora do turno, **1 reação** por rodada.
   - Ações: atacar, conjurar, defender (+4 Defesa até o próximo turno), usar item, preparar uma ação, ajudar (dá vantagem a um aliado), fugir (movimento duplo).
   - Reações: ataque de oportunidade (alguém sai do seu alcance ou encanta adjacente a você), aparar/esquivar com técnica, contra-golpe (Estilo Deus da Água).

### Distância importa
| Faixa | Distância | Notas |
|---|---|---|
| Corpo a corpo | até 2 m | encantar aqui provoca ataque de oportunidade |
| Curta | até 10 m | 1 movimento até o corpo a corpo |
| Média | até 30 m | 2–3 turnos até o corpo a corpo; arcos e magias de projétil confortáveis |
| Longa | até 100 m | só magias de alcance longo, arcos longos e olhos treinados |
| Extrema | além | artilharia mágica de ranks altos |
- **Magos de perto são vulneráveis**: encantar em corpo a corpo provoca ataque de oportunidade e dá desvantagem no teste de interrupção.
- **Espadachins de longe são vulneráveis**: cada turno atravessando a faixa média é um turno inteiro de magia contra eles. Cobertura (+2 ou +5 Defesa) e terreno são a resposta.

### Ataque, Defesa e dano
- **Ataque físico**: `1d20 + Força (armas pesadas) ou Agilidade (leves) + rank do estilo` contra **Defesa**.
- **Defesa** = `10 + Agilidade + bônus do rank do estilo usado para defender (ou metade, sem estilo) + armadura/escudo`.
- **Dano físico** = `dado da arma + atributo + bônus de rank do estilo`.
- **Crítico** (20 natural): dano máximo do dado da arma + uma rolagem extra do dado; o Mestre pode pedir rolagem de ferimento no alvo.
- **Aura de batalha (touki)**: a partir do rank **Avançado** em qualquer estilo, **redução de dano físico** = metade do bônus de rank (Avançado 2, Santo 3, Rei 4, Imperador 6, Deus 7), e metade disso contra magia. No rank Santo ou acima, gastar 3 mana dá +bônus de rank num teste físico (salto, força, velocidade).

### Estatísticas rápidas por rank (NPCs)
| Rank | Ataque | Defesa | PV | Dano típico | Redução |
|---|---|---|---|---|---|
| Sem treino | +1 | 10 | 8 | 1d6 | 0 |
| Iniciante | +3 | 12 | 14 | 1d8+2 | 0 |
| Intermediário | +5 | 14 | 20 | 1d8+4 | 0 |
| Avançado | +8 | 16 | 30 | 1d10+6 | 2 |
| Santo | +11 | 19 | 45 | 2d8+8 | 3 |
| Rei | +15 | 22 | 65 | 2d10+12 | 4 |
| Imperador | +19 | 25 | 90 | 3d10+15 | 6 |
| Deus | +24 | 29 | 130 | 4d10+20 | 7 |

### Ferimentos persistentes
- Quando um único golpe causa dano **≥ metade do PV máximo**, ou quando os PV chegam a **0**, role `python scripts/dados.py ferimento --gravidade <leve|grave|critico>` (golpe pesado: leve ou grave; 0 PV: grave ou crítico, a critério da cena).
- Registre em `personagem.ferimentos_persistentes`. Ferimentos persistentes **não somem com descanso**.

### 0 PV e morte
- Em 0 PV: inconsciente e morrendo. A cada rodada, `1d20 + Vigor` CD 10: 3 sucessos = estável; 3 falhas = **morte**. Um 20 natural acorda com 1 PV.
- Qualquer cura de pelo menos 1 PV estabiliza e acorda.
- **Nenhuma magia ressuscita.** A morte do personagem é permanente. O Mestre deixa claro quando uma situação é mortal antes de o jogador se comprometer com ela.

## 7. Cura e seus limites
| Ferimento | Cura mínima | Sem magia |
|---|---|---|
| Leve | Cura Intermediária | dias a semanas |
| Grave | Cura Avançada | meses, muitas vezes com sequela |
| Crítico | Cura Santa (alguns só Rei) | permanente ou fatal |
- Regenerar membros perdidos exige **Cura de rank Rei** (pouquíssimos no mundo).
- Descanso natural: `2 + Vigor` PV por dia (mínimo 1), aplicado pelo `avancar_tempo.py --descanso`.

## 8. Viagem, tempo e descanso
- O tempo do mundo avança com `python scripts/avancar_tempo.py` em viagens, treinos e descansos longos. Os relógios do mundo andam com ele.
- Viagens têm tempo e perigo (`dados/locais.json`). A cada 7 dias de estrada, o Mestre rola 1d10; resultado ≤ perigo da rota = encontro.
- Comida, dinheiro, montaria e guia importam em viagens longas. Cansaço acumulado: −1 em testes físicos por dia sem descanso adequado.
- **Sono e sonhos**: toda noite pode importar. Onde, com quem e protegido por quem o personagem dorme pode ter consequências. Se o personagem sonha, o Mestre narra o sonho ao acordar e o registra; se é Sem-Sonho, a ausência também é narrada.

## 9. Treino e progressão (`/treinar`)

### Subir de rank
| Passo | Tempo mínimo | Mentor necessário | CD do teste |
|---|---|---|---|
| Nenhum → Iniciante | 1 mês | qualquer treinado (ou livro, para magia) | 10 |
| Iniciante → Intermediário | 3 meses | Intermediário ou acima | 14 |
| Intermediário → Avançado | 1 ano | Avançado ou acima | 18 |
| Avançado → Santo | 3 anos | Santo ou acima (ou evento marcante + 1 ano) | 22 |
| Santo → Rei | 5 anos | Rei ou acima, ou evento extraordinário | 26 |
| Rei → Imperador | 10 anos | só com algo que mude o mundo | 30 |
| Imperador → Deus | — | apenas narrativo | — |
- **Teste**: `1d20 + atributo principal (Intelecto para magia; Força ou Agilidade para espada) + bônus do rank atual`.
- **Modificadores**: mentor dois ranks acima do alvo +2; evento marcante ligado ao treino +2; cada metade extra do tempo mínimo +1; treino em condições ruins (fuga, fome) −2.
- **Crianças até 12 anos** treinam magia na metade do tempo.
- **Sem mentor**: tempo dobrado; sozinho, ninguém passa de Intermediário (de Avançado, com biblioteca de universidade, em magia).
- **Falha**: o tempo foi gasto e conta como progresso parcial; novo teste após mais 1/4 do tempo mínimo.

### Aprender magias e técnicas
- **Magia nova** do seu rank ou abaixo, com livro ou professor: dias = custo de mana × 2; teste de Intelecto + rank, CD 10 + 2 por rank da magia (Iniciante 12, Intermediário 14, Avançado 16, Santo 18…).
- **Técnica nova** do seu rank ou abaixo, com mentor do estilo: semanas = 2 × posição do rank (Iniciante 2, Intermediário 4…); teste de Força/Agilidade + rank, mesma CD.
- **Conjuração silenciosa**: até os 10 anos, 6 meses de prática e CD 15; dos 11 aos 15, 1 ano e CD 20; adultos, 2 anos e CD 25 (quase ninguém consegue).
- **Capacidade de mana**: cresce sozinha com treino (tabela da seção 4); o Mestre aplica o ganho em `mana_max` a cada ano de prática.
- **Idiomas**: 6 meses de convivência ou 3 meses com professor para o básico.

### Reputação na Guilda
| Rank | F | E | D | C | B | A | S |
|---|---|---|---|---|---|---|---|
| Pontos para alcançar | 0 | 10 | 30 | 80 | 200 | 500 | 1200 |
Missões dão de 1 (rank F) a 50+ pontos (rank S). Falhas e abandonos tiram pontos.

## 10. Dinheiro
| Moeda | Valor |
|---|---|
| `cobre` | unidade básica |
| `prata` | 10 cobre |
| `ouro_asura` | 10 prata (moeda de prestígio do Central) |
| `prata_millis` | 1 prata (aceita em Millis e portos) |
| `ferro_demonio` | 5 = 1 cobre (Continente Demoníaco; escambo é comum) |
Referências: refeição 2 cobre; quarto de estalagem 5 cobre; espada comum 3 prata; cavalo 4 ouro; passagem pelo estreito 5 prata; travessia oceânica 3–8 ouro; mentor Avançado por mês 3 ouro; um ano na Universidade de Ranoa 15 ouro (bolsas existem).

## 11. Idiomas
Língua Humana (comum do Central e de Millis), Língua Demoníaca, Língua dos Povos-Fera, Língua Celestial, Língua do Mar, Língua Litúrgica de Millis (escrita sacra), Dragônico Antigo (só em ruínas e com raríssimos falantes).

## 12. Personagens da party (NPCs)
Usam a tabela de estatísticas por rank, com PV e lealdade registrados em `campanha/party.json`. Lealdade (−100 a 100) cai com abandono, mentira descoberta e risco desnecessário; sobe com proteção, confiança e escolhas que respeitam os objetivos deles. Abaixo de 0 eles vão embora (ou pior). NPCs não existem para servir: têm objetivos próprios e podem recusar ordens.
