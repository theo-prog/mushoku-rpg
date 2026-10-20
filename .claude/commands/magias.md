---
description: Lista magias (conhecidas ou do catálogo)
argument-hint: [conhecidas | <escola> [rank]]
---
Argumentos: `$ARGUMENTS`

- Sem argumento ou `conhecidas`: `python scripts/sessao.py magias --conhecidas`.
- Com escola (fogo, agua, terra, vento, combinada, cura, desintoxicacao, barreira, invocacao) e/ou rank: `python scripts/sessao.py magias --escola <escola> [--rank <rank>]`.

Apresente em lista curta: nome, rank, custo de mana, tempo de conjuração, alcance, efeito resumido e se aceita conjuração silenciosa. Para magias que o personagem **não** conhece, mostre só o que ele poderia saber (livros, aulas, rumores). Magias de rank Rei ou acima são lendas: apresente como tal.
