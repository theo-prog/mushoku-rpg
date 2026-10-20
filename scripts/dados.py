"""Rolagens de dados da campanha. Todo resultado deve ser mostrado ao jogador.

Uso:
  python scripts/dados.py 1d20+3 [--vantagem|--desvantagem] [--cd 15] [--rotulo "Escalar o muro"]
  python scripts/dados.py 2d6+1d4-1 --rotulo "Dano da adaga"
  python scripts/dados.py 4d6kh3                      (mantém os 3 maiores)
  python scripts/dados.py teste agilidade --rank espada.deus_da_agua --cd 15 [--mod -2] [--vantagem]
  python scripts/dados.py teste intelecto --rank magia.fogo --cd 12
  python scripts/dados.py ferimento [--gravidade leve|grave|critico]
"""
import argparse
import random
import re
from datetime import datetime

import rpgcomum as rc

TERMO = re.compile(r"([+-]?)\s*(?:(\d*)d(\d+)(k[hl]\d+)?|(\d+))")

FERIMENTOS = {
    "leve": [
        "Corte profundo no antebraço: -1 em testes de Força por 2 semanas.",
        "Costela trincada: -1 em Vigor e em testes de esforço até curar (Cura Intermediária ou 1 mês).",
        "Entorse no tornozelo: deslocamento reduzido à metade por 1 semana.",
        "Concussão: desvantagem em Percepção por 3 dias.",
        "Queimadura extensa: -1 em Presença até cicatrizar; deixa marca.",
        "Dedo quebrado na mão dominante: -1 em ataques e gestos de conjuração por 2 semanas.",
    ],
    "grave": [
        "Fratura exposta na perna: não corre; precisa de Cura Avançada ou 3 meses.",
        "Olho ferido: desvantagem em ataques à distância até Cura Avançada; sem ela, cegueira parcial permanente.",
        "Tendão rompido no braço: arma de duas mãos impossível; Cura Avançada ou 4 meses com sequela (-1 Força).",
        "Hemorragia interna: perde 1 PV por hora até receber cura; depois -2 PV máximos por 1 mês.",
        "Canal de mana lesionado: custo de magias +2 até Cura Avançada ou 2 meses de repouso.",
        "Cicatriz na garganta: encantações em voz alta exigem teste de Vigor CD 12 por 1 mês.",
    ],
    "critico": [
        "Membro decepado (mão ou braço): só Cura de rank Rei regenera; caso contrário, permanente.",
        "Perna esmagada: Cura Santa evita amputação; sem ela, perda do membro.",
        "Perda de um olho: permanente salvo Cura de rank Rei.",
        "Núcleo de mana rachado: mana máxima -25% permanente salvo tratamento de rank Santo.",
        "Pulmão perfurado: inconsciente; morte em 1d6 turnos sem Cura Avançada.",
        "Coluna atingida: paralisia das pernas; só Cura de rank Rei reverte.",
    ],
}


def rolar_expr(expr, vantagem=False, desvantagem=False):
    expr = expr.replace(" ", "").lower()
    pos, partes, total, d20_natural = 0, [], 0, None
    usou_vant = False
    while pos < len(expr):
        m = TERMO.match(expr, pos)
        if not m or m.end() == pos:
            raise SystemExit(f"Expressão inválida perto de: {expr[pos:]!r}")
        sinal = -1 if m.group(1) == "-" else 1
        if m.group(5) is not None:
            v = int(m.group(5)) * sinal
            total += v
            partes.append(f"{'+' if sinal > 0 else '-'}{abs(v)}")
        else:
            n = int(m.group(2) or 1)
            faces = int(m.group(3))
            if n > 200 or faces > 1000:
                raise SystemExit("Dados demais.")
            if faces == 20 and n == 1 and (vantagem or desvantagem) and not usou_vant:
                a, b = random.randint(1, 20), random.randint(1, 20)
                escolhido = max(a, b) if vantagem else min(a, b)
                usou_vant = True
                d20_natural = escolhido
                rot = "vant" if vantagem else "desv"
                partes.append(f"{'+' if sinal > 0 else '-'}1d20[{a},{b}→{escolhido} {rot}]")
                total += sinal * escolhido
            else:
                rolls = [random.randint(1, faces) for _ in range(n)]
                mantidos = rolls
                if m.group(4):
                    k = int(m.group(4)[2:])
                    mantidos = sorted(rolls, reverse=m.group(4)[1] == "h")[:k]
                if faces == 20 and n == 1 and d20_natural is None:
                    d20_natural = rolls[0]
                s = sum(mantidos)
                total += sinal * s
                extra = f"→{mantidos}" if m.group(4) else ""
                partes.append(f"{'+' if sinal > 0 else '-'}{n}d{faces}{m.group(4) or ''}{rolls}{extra}")
        pos = m.end()
    txt = " ".join(partes).lstrip("+")
    return total, txt, d20_natural


def veredito(total, cd, nat):
    if nat == 20:
        return "SUCESSO CRÍTICO (20 natural)"
    if nat == 1:
        return "FALHA CRÍTICA (1 natural)"
    if total >= cd + 10:
        return "SUCESSO EXCEPCIONAL"
    if total >= cd:
        return "SUCESSO"
    if total >= cd - 2:
        return "PARCIAL (consegue com custo, ou falha por pouco)"
    return "FALHA"


def registrar(linha):
    try:
        data = rc.ler(rc.camp("estado")).get("data_mundo", "?")
    except Exception:
        data = "?"
    try:
        with open(rc.CAMPANHA / "rolagens.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M} | mundo {data} | {linha}\n")
    except Exception:
        pass


def bonus_rank(caminho):
    if caminho is None:
        return 0, ""
    if re.fullmatch(r"[+-]?\d+", caminho):
        return int(caminho), f"rank {caminho}"
    p = rc.ler(rc.camp("personagem"))
    no = p.get("ranks", {})
    for parte in caminho.split("."):
        no = no.get(parte, "nenhum") if isinstance(no, dict) else "nenhum"
    rank = no if isinstance(no, str) else "nenhum"
    return rc.RANK_BONUS.get(rank, 0), f"{caminho}={rank}"


def main():
    rc.utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("expr")
    ap.add_argument("atributo", nargs="?")
    ap.add_argument("--vantagem", action="store_true")
    ap.add_argument("--desvantagem", action="store_true")
    ap.add_argument("--cd", type=int)
    ap.add_argument("--rotulo", default="")
    ap.add_argument("--rank")
    ap.add_argument("--mod", type=int, default=0)
    ap.add_argument("--gravidade", choices=list(FERIMENTOS))
    a = ap.parse_args()
    if a.vantagem and a.desvantagem:
        a.vantagem = a.desvantagem = False

    if a.expr == "ferimento":
        grav = a.gravidade or random.choice(["leve", "leve", "grave", "grave", "critico"])
        i = random.randint(1, 6)
        linha = f"FERIMENTO ({grav}) 1d6={i}: {FERIMENTOS[grav][i - 1]}"
        print(linha)
        registrar(linha)
        return

    if a.expr == "teste":
        if a.atributo not in rc.ATRIBUTOS:
            raise SystemExit(f"Atributo inválido. Use: {', '.join(rc.ATRIBUTOS)}")
        p = rc.ler(rc.camp("personagem"))
        mod_attr = int(p.get("atributos", {}).get(a.atributo, 0))
        b, desc = bonus_rank(a.rank)
        expr = f"1d20{mod_attr:+d}{b:+d}{a.mod:+d}"
        rot = a.rotulo or f"Teste de {a.atributo}" + (f" ({desc})" if desc else "")
    else:
        expr, rot = a.expr, a.rotulo

    total, txt, nat = rolar_expr(expr, a.vantagem, a.desvantagem)
    linha = f"{rot + ': ' if rot else ''}{expr} → {txt} = {total}"
    if a.cd is not None:
        linha += f" vs CD {a.cd} → {veredito(total, a.cd, nat)}"
    print(linha)
    registrar(linha)


if __name__ == "__main__":
    main()
