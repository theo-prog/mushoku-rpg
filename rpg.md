# Tarefa: construir um Mestre de RPG solo no universo de Mushoku Tensei — "O Ano Sem Sonhos"

Crie, nesta pasta, um sistema completo para você (Claude Code) atuar como **Mestre de RPG** em uma campanha solo ambientada no universo de *Mushoku Tensei*, em uma **linha do tempo alternativa**: mesmo mundo, mesma magia, mesmas raças, facções e geografia, porém **sem Rudeus Greyrat, sem a família Greyrat como protagonista e sem os eventos canônicos da história principal**. Os acontecimentos são novos; o "DNA" do mundo é o original.

Leia este documento inteiro antes de começar. Execute na ordem da seção 10.

---

## 1. Estrutura de arquivos

```
CLAUDE.md                     # regras do Mestre (lido em toda sessão)
lore/                         # texto de referência (não muda durante o jogo)
  mundo.md                    # cosmologia, história antiga, continentes
  magia.md                    # sistema de magia
  combate.md                  # estilos de espada, aura de batalha, ranks
  racas.md                    # raças e relações entre elas
  faccoes.md                  # reinos, igreja, guildas, Sete Grandes Poderes
  divergencia.md              # tudo que é "desta realidade"
regras/
  sistema.md                  # mecânica de jogo
dados/                        # catálogos fixos (consultados sob demanda)
  magias.json
  estilos_espada.json
  racas.json
  itens.json
  monstros.json
  locais.json                 # cidades, labirintos, rotas, tempo de viagem
historia/                     # campanha pré-pronta
  linha_do_tempo.json
  arcos.json
  segredos.json               # NUNCA mostrar ao jogador
campanha/                     # estado mutável
  estado.json
  personagem.json
  party.json
  npcs.json
  faccoes_estado.json
  quests.json
  inventario.json
  diario.md
schemas/                      # JSON Schema de cada arquivo JSON acima
scripts/
  dados.py                    # rolagens (1d20+3, 2d6, vantagem/desvantagem)
  validar.py                  # valida todos os JSON contra schemas/
  backup.py                   # snapshot de campanha/ em backups/AAAA-MM-DD_HHMM/
  avancar_tempo.py            # avança a data e dispara eventos da linha do tempo
backups/
.claude/commands/
  rolar.md  ficha.md  salvar.md  carregar.md  mapa.md  recap.md
  descansar.md  magias.md  inventario.md  quests.md  faccoes.md
  viajar.md  treinar.md
```

---

## 2. Fidelidade ao universo (escreva em `lore/`)

**Cosmologia e história**
- O mundo era originalmente o **Mundo de Seis Faces**, cada face com sua raça e seu deus; foi destruído em eras antigas e hoje resta um mundo unificado com marcas dessa história.
- Guerras históricas entre humanos e demônios, incluindo a **Guerra de Laplace**, que deixou ódio duradouro (ex: perseguição aos **Superd**).
- O **Deus Humano (Hitogami)** existe como entidade misteriosa que aparece em sonhos dando "conselhos". É manipulador por natureza.

**Geografia**
- **Continente Central**: Reino de Asura, Região dos Conflitos, Montanhas do Dragão Vermelho, Reino do Rei Dragão, Shirone, Ranoa e a Universidade de Magia em Sharia, Três Nações Mágicas.
- **Continente Demoníaco**: terreno hostil, monstros fortes, Reis Demônio locais.
- **Continente de Millis**: Sagrado Reino de Millis, Grande Floresta dos povos-fera.
- **Continente de Begaritt**: deserto e labirintos.
- **Continente Celestial** e **Mar de Ringus**.
- Viagens são **longas e perigosas**: atravessar continentes leva meses ou anos. Isso é central para o tom. Registre tempos de viagem em `locais.json`.

**Magia**
- Escolas: ataque (fogo, água, terra, vento e combinações), cura, desintoxicação, barreira, invocação; magia divina ligada à igreja.
- Ranks: Iniciante → Intermediário → Avançado → Santo → Rei → Imperador → Deus. Cada salto é **raro e difícil**.
- **Encantação** é o padrão; **conjuração silenciosa** é rara e marca de talento excepcional.
- A **capacidade de mana** cresce com treino principalmente na infância; adultos evoluem mais devagar.
- Círculos mágicos, pedras mágicas, itens mágicos, **Olhos Demoníacos**, **Bênçãos Divinas** e **Maldições** como traços raros e marcantes.

**Combate físico**
- **Estilo Deus da Espada**: ofensiva, velocidade, primeiro golpe.
- **Estilo Deus da Água**: defesa e contra-ataque.
- **Estilo Deus do Norte**: imprevisível, adaptável, usa qualquer truque.
- Mesmos ranks da magia.
- **Aura de batalha (touki)**: guerreiros de alto nível reforçam o corpo com mana; é o que permite enfrentarem magos.

**Raças**: humanos, demônios (Migurd, Superd e muitas outras), povos-fera (ex: tribo Dedoldia), elfos, anões, halflings, raça celestial, raça do mar, raça dragão. Preconceito racial é motor de conflito.

**Facções**
- **Os Sete Grandes Poderes**: títulos dos sete seres mais fortes (Deus Técnico, Deus Dragão, Deus da Luta, Deus Demônio, Deus da Morte, Deus da Espada, Deus do Norte). Nesta realidade, quem ocupa cada título é definido por você em `divergencia.md`.
- **Imperadores e Reis Demônio**: governantes excêntricos e longevos do Continente Demoníaco.
- **Igreja de Millis**: dividida internamente (Cavaleiros do Templo, Cavaleiros da Catedral etc.), forte poder político.
- **Reino de Asura**: rico, decadente, intrigas de nobreza e sucessão.
- **Guilda de Aventureiros**: ranks F a S, missões, reputação de party.
- **Universidade de Magia de Ranoa**.
- **Labirintos**: masmorras com núcleo mágico, armadilhas e tesouros.

Se algo da lore for incerto, seja fiel ao espírito do mundo em vez de inventar detalhes canônicos falsos, e registre como "desta realidade" em `divergencia.md`.

---

## 3. Tom da narrativa

- **Escala humana primeiro**: jornada pessoal, crescimento lento, relações, consequências. Não é power fantasy instantâneo.
- **O mundo é cruel e indiferente**: morte, perda e separação acontecem. Escolhas têm custo real e permanente.
- **Grandes elipses de tempo** são normais (treinos de anos, viagens de meses). Ofereça saltos de tempo com resumo do que mudou.
- **Hierarquia de poder clara**: rank Avançado não vence rank Rei. Encontros com os Sete Grandes Poderes devem ser aterrorizantes.
- Mistura de cotidiano (aulas, guilda, refeições, conversas) com crises intensas.
- NPCs com motivações próprias, falhas e arcos. Nenhum NPC existe só para servir ao jogador.

---

## 4. Exclusões (versão sem polêmicas)

- **Nenhum conteúdo sexual ou sexualizado envolvendo menores de idade**, nunca, nem implícito, nem como piada.
- Sem fanservice, voyeurismo, "humor pervertido" ou comportamento predatório normalizado.
- Romance apenas entre personagens adultos, tratado com elipse ("fade to black").
- Escravidão, racismo e violência existem como **problemas do mundo**, retratados com peso, nunca glorificados ou usados como recompensa.
- O personagem não é obrigatoriamente reencarnado. Se o jogador quiser, permita, sem reproduzir o passado ou a personalidade do protagonista canônico.
- Encantações, nomes de técnicas e textos devem ser **originais**, inspirados no estilo do mundo, nunca copiados da obra.

---

## 5. Sistema de jogo (`regras/sistema.md`)

- **Atributos**: Força, Agilidade, Vigor, Intelecto, Percepção, Presença.
- **Testes**: `1d20 + modificador + bônus de rank` contra CD definida pelo Mestre. Vantagem/desvantagem = rolar 2d20 e pegar o maior/menor.
- **Ranks substituem níveis**: subir de rank exige treino, mentor ou evento marcante, nunca só XP. Use `/treinar` com tempo de jogo e testes.
- **Mana**: recurso finito, recupera com descanso; feitiços de rank maior custam mais; conjuração silenciosa dá vantagem/iniciativa.
- **Ferimentos persistentes** e cura mágica com limites (não ressuscita).
- **Combate**: iniciativa, ações por turno, distância importa (magos vulneráveis de perto, espadachins de longe).
- **Toda rolagem usa `scripts/dados.py`** e o resultado é mostrado ao jogador.

---

## 6. Persistência e dados estruturados

**Regras gerais**
- Todo arquivo em `dados/`, `historia/` e `campanha/` tem JSON Schema em `schemas/`. Rode `validar.py` após cada escrita; se falhar, corrija antes de continuar.
- `/salvar` = atualizar `campanha/`, rodar `validar.py`, rodar `backup.py`, adicionar entrada no `diario.md`.
- `/carregar` (e início de sessão) = ler `campanha/` + últimas 3 entradas do diário + arcos ativos. Catálogos são consultados sob demanda, não carregados inteiros.
- Nunca apagar entradas: NPCs mortos, quests falhadas e facções destruídas mudam de `status`.
- IDs em snake_case, únicos, referenciados entre arquivos.

**Campos mínimos**

`personagem.json`: id, nome, raça, idade, data_nascimento_mundo, origem, sem_sonho(bool), atributos{6}, pv/pv_max, mana/mana_max, capacidade_mana_crescimento, ranks{magia por escola, espada por estilo}, magias_conhecidas[ids], tecnicas[ids], encantacao_silenciosa(bool), tracos[bênçãos, maldições, olhos demoníacos], ferimentos_persistentes[], idiomas[], reputacao_guilda{rank, pontos}, dinheiro{moedas por tipo}, objetivos[], relacoes{npc_id: -100..100}, sonhos_registrados[].

`magias.json` (cada entrada): id, nome, escola, rank, custo_mana, encantacao (texto curto original), tempo_conjuracao, alcance, efeito, dano(dados), requisitos, pode_silenciosa(bool).

`estilos_espada.json`: id, nome, escola, rank, efeito, custo, requisitos.

`faccoes_estado.json`: id, nome, tipo, lider_npc_id, sede_local_id, poder(0-10), atitude_com_jogador(-100..100), postura_sem_sonho, relacoes{faccao_id: valor}, objetivos_publicos[], objetivos_ocultos[], status.

`npcs.json`: id, nome, raça, idade, rank, faccao_id, local_atual, atitude, personalidade, voz (jeito de falar), frase_caracteristica, objetivos, segredos[], oco(bool, oculto), conhecido_pelo_jogador(bool), status(vivo/morto/desaparecido/oco).

`estado.json`: data_mundo, local_atual, clima, relogios{id: estagio}, flags[], noticias_recentes[].

`linha_do_tempo.json`: id, data_mundo, titulo, descricao, local_id, faccoes_envolvidas[], relogio_id, status(futuro/ocorrendo/ocorrido/evitado/alterado), alteravel_pelo_jogador(bool), consequencias[].

`arcos.json`: id, titulo, ato, tipo(principal/secundario), gatilho, fases[{descricao, objetivo, saidas_possiveis}], pistas[{revelacao_id, local_id, descricao}], npcs_chave[], recompensas, status.

`quests.json`, `inventario.json`, `party.json`, `monstros.json`, `itens.json`, `locais.json`, `racas.json`: estrutura equivalente, com IDs referenciando os catálogos.

**Catálogos iniciais**
- `magias.json`: no mínimo 8 magias por rank em cada escola de ataque até Santo; cura, desintoxicação, barreira e invocação até Avançado. Rei+ poucas e lendárias.
- Técnicas para as três escolas de espada até Santo.
- Bestiário com 40+ criaturas distribuídas por continente, incluindo criaturas ligadas à crise atual.
- Locais principais de todos os continentes com rotas e tempos de viagem.

---

## 7. História pré-pronta: "O Ano Sem Sonhos"

### 7.1 Premissa (conhecimento público no mundo)
Há 13 anos, numa noite conhecida como **A Noite Muda**, ninguém no mundo sonhou. Nenhum humano, demônio, fera ou elfo. Todos acordaram com a sensação de que algo havia passado por eles enquanto dormiam.

Desde então:
- Crianças nascidas depois daquela noite, os **Sem-Sonho**, às vezes apresentam capacidade de mana anormal. Muitos nunca sonham. Alguns sonham coisas que ainda não aconteceram.
- No Mar de Ringus surgiu uma **ilha invertida**, suspensa no céu de cabeça para baixo, que desce alguns metros a cada ano. Marinheiros dizem ouvir sinos vindos dela. Nenhuma expedição voltou inteira.
- Surgiram os **Ocos**: pessoas que, numa manhã qualquer, continuam vivendo, trabalhando e sorrindo, mas não estão mais ali. Não comem quando ninguém olha. Não piscam no escuro. Às vezes aldeias inteiras amanhecem com todos os Ocos de pé, imóveis, voltados para a mesma direção. Ninguém sabe quem já é Oco até ser tarde.
- Os sonhos voltaram, mas há relatos de **duas vozes** falando com pessoas enquanto dormem. Uma oferece conselhos gentis e precisos. A outra fala de baixo, de muito fundo, e diz a verdade de forma cruel. As duas acusam a outra de ter causado a Noite Muda.

Registre a Noite Muda e todas as consequências em `divergencia.md`.

### 7.2 Relógios (o mundo avança sem o jogador)
Cada relógio tem estágios em `linha_do_tempo.json` e piora se ninguém agir:
1. **A Descida**: a ilha invertida desce até tocar o mar. O que acontece então é desconhecido.
2. **A Coroa Silenciosa**: em Asura, rumores de que o rei virou Oco e a corte governa à sua volta, escondendo isso. Casas nobres se preparam para uma sucessão sangrenta.
3. **A Purificação**: a Igreja de Millis está dividida entre declarar os Sem-Sonho abominações ou santos. A ala que vencer define se haverá cruzada ou proteção.
4. **O Título Vago**: o **Deus da Espada** foi morto há 3 anos por alguém usando uma técnica de nenhuma escola conhecida. O título está vago; duelistas caçam o assassino e uns aos outros.
5. **A Migração**: os Ocos estão lentamente caminhando. Todos na mesma direção.

`avancar_tempo.py` dispara os eventos quando a data chega; o Mestre narra as consequências conforme o jogador ouve notícias ou chega aos locais.

### 7.3 Facções diante da crise
Para cada uma, defina o que **mostra**, o que **quer de verdade** e o que **fará com o jogador** se ele for (ou parecer ser) um Sem-Sonho:
- **Reino de Asura**: quer Sem-Sonhos como armas; esconde o estado do rei.
- **Igreja de Millis**: facção purista (caça) vs. facção mística (protege como profecia). Crie um **inquisidor carismático**, moralmente cinza, que caça o jogador por motivos que façam sentido.
- **Universidade de Ranoa**: estuda os Sem-Sonhos; há professores fazendo experimentos que não deveriam.
- **Imperadores e Reis Demônio**: alguns oferecem refúgio, outros querem os Sem-Sonhos por razões antigas. Um deles se lembra de algo parecido com a Noite Muda de uma era anterior.
- **Grande Floresta e povos-fera**: os Ocos não entram na floresta. Ninguém sabe por quê, e os anciões não falam.
- **Guilda de Aventureiros**: paga muito bem por missões ligadas a Ocos e à ilha; ninguém comenta a taxa de mortalidade.
- **Os Sete Grandes Poderes**: cada um tem posição própria. Pelo menos um ajuda, pelo menos um atrapalha, e pelo menos um não se importa, o que é mais assustador.
- **Os Acordados**: culto que ouve a voz de baixo e acredita que os Ocos são o próximo passo, não uma doença.

### 7.4 Aberturas
O jogador escolhe uma origem; cada uma tem cena de abertura própria, e todas convergem para o mesmo evento em até 2 sessões:
- **Aldeia de fronteira**: na manhã do festival da colheita, o personagem acorda e encontra todos os adultos da aldeia de pé dentro do rio, em silêncio, olhando para o oeste. Exceto um, que sussurra: "corra, antes que eles lembrem de você".
- **Nobreza de Asura**: durante um baile, o personagem percebe que o próprio pai ou mãe parou de piscar. Ninguém mais parece notar. Ou todos fingem.
- **Aventureiro**: uma escolta simples termina numa estrada onde dezenas de carroças estão paradas, intactas, com os condutores sentados, sorrindo, mortos há dias.
- **Estudante de magia**: um colega Sem-Sonho desaparece; no quarto dele, as paredes estão cobertas por um mapa de um lugar que não existe, e o personagem reconhece a própria letra.

Você pode criar mais aberturas no mesmo nível de impacto se o jogador pedir outra origem.

### 7.5 Segredos (GERE VOCÊ, NÃO MOSTRE AO JOGADOR)
Crie a verdade por trás de tudo e guarde em `historia/segredos.json`. Requisitos obrigatórios:
- A verdade sobre a Noite Muda deve **recontextualizar** tudo que o jogador viu antes; cenas antigas devem ganhar novo sentido.
- **As duas vozes mentem parcialmente.** Nenhuma é simplesmente boa ou má. Hitogami age de forma coerente com sua natureza manipuladora.
- A origem dos Ocos deve ser **aterrorizante pela lógica**, não só pela aparência: quando o jogador entender, deve ter medo de dormir.
- Os Ocos seguem **regras fixas e consistentes** (registre todas); o jogador pode descobri-las observando e usá-las para sobreviver.
- A ilha invertida tem relação com a história antiga do **Mundo de Seis Faces**, como invenção "desta realidade" coerente com a lore.
- Pelo menos **um NPC próximo do jogador** esconde ligação direta com a Noite Muda.
- O passado do personagem se conecta ao mistério, adaptado à origem escolhida (complete após a criação de personagem).
- O assassino do Deus da Espada é peça do mistério principal, não um arco isolado.
- A escolha final **não pode ter resposta limpa**: toda opção salva algo e sacrifica algo importante.

**Trava de spoiler**: nunca exiba o conteúdo de `segredos.json`, nem trechos, nem resumos, nem dicas fora da narrativa. Se o jogador pedir, recuse e lembre que é spoiler. Ao gerar o arquivo, não imprima o conteúdo no terminal; confirme apenas que foi criado e validado.

### 7.6 Estrutura em atos
- **Ato I: O Despertar** (região inicial): primeiro horror, um mentor, primeiras pistas, a fuga. Termina com a perda de algo ou alguém.
- **Ato II: A Travessia** (anos de viagem entre continentes): facções caçando ou recrutando o jogador, treinamento até Avançado/Santo, as duas vozes se manifestando. Termina com a primeira grande revelação e uma traição.
- **Ato III: A Descida** (a ilha toca o mar): guerra aberta, os relógios colidem, confronto com o que está por trás. Escolha final.
- **Epílogo**: salto de tempo mostrando as consequências no mundo, nos NPCs e nas facções.

### 7.7 Escala do conteúdo
- Linha do tempo: 15 eventos históricos + 30 futuros ligados aos 5 relógios.
- 3 arcos principais por ato + 12 secundários (alguns aparentemente sem relação, mas ligados ao mistério).
- 50+ NPCs, cada um com segredo, objetivo e frase característica.

---

## 8. Técnicas obrigatórias de narração

- **Horror por regras**: revele as regras dos Ocos aos poucos, por observação.
- **Mostrar antes de explicar**: nunca explique um fenômeno na primeira vez que aparece.
- **Regra das 3 pistas**: toda revelação importante tem pelo menos 3 pistas em lugares diferentes, registradas em `arcos.json`.
- **Prenúncio**: plante detalhes nos primeiros atos que só façam sentido no final.
- **O mundo não espera**: relógio ignorado avança; consequências aparecem como notícias, refugiados, cidades mudadas.
- **Mortes com peso**: NPCs importantes podem morrer, nunca de forma gratuita; cada morte muda algo.
- **Respiro**: depois de cena intensa, cena tranquila (refeição, conversa, treino). O contraste sustenta o horror e o drama.
- **Pequeno e pessoal dentro do épico**: toda ameaça global tem um rosto que o jogador conhece.
- **Sonhos como mecânica**: se o personagem sonha, narre os sonhos ao acordar e registre em `sonhos_registrados`. Se é Sem-Sonho, a ausência também é narrada e notada por NPCs.

---

## 9. Comportamento do Mestre (`CLAUDE.md`)

- Ao iniciar sessão: executar o fluxo de `/carregar` e abrir com recap curto.
- Narrar em português, em segunda pessoa, com descrições sensoriais e diálogos de NPC com voz própria.
- **Nunca decidir ações, falas ou sentimentos do personagem do jogador.**
- Terminar cada turno com uma situação aberta, não com lista fixa de opções (opções só se o jogador pedir).
- Consultar `lore/` antes de inventar algo grande; registrar novidades em `divergencia.md`.
- Atualizar `campanha/` ao final de cada cena relevante e sempre no `/salvar`.
- Esconder o que o personagem não sabe; segredos de NPCs e `segredos.json` nunca aparecem fora da narrativa.
- Jogar justo: se o dado falhar, a falha acontece.
- Respeitar a seção 4 em qualquer situação.
- Avançar a data do mundo com `avancar_tempo.py` em viagens, treinos e descansos longos.

---

## 10. Ordem de execução

Faça em etapas, rodando `validar.py` ao final de cada uma e corrigindo erros antes de seguir:
1. Estrutura de pastas, `schemas/`, scripts (`dados.py`, `validar.py`, `backup.py`, `avancar_tempo.py`) e comandos em `.claude/commands/`.
2. `lore/` e `regras/sistema.md`.
3. Catálogos em `dados/`.
4. `historia/segredos.json` (sem imprimir o conteúdo).
5. Facções (`faccoes_estado.json`) e NPCs (`npcs.json`).
6. `linha_do_tempo.json` com os 5 relógios.
7. `arcos.json` com pistas.
8. `CLAUDE.md`.
9. Testar: uma rolagem, um `/salvar`, um `/carregar` e um `avancar_tempo.py` de 30 dias num estado de teste; depois resetar `campanha/`.

Quando tudo estiver pronto, me avise e inicie a **criação de personagem** em forma de conversa: origem (seção 7.4), raça, idade inicial, se é Sem-Sonho, região, treino na infância, ranks iniciais e ambição. Então complete o vínculo do personagem em `segredos.json` e comece a campanha pela cena de abertura.