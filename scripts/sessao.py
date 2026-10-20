"""Visões rápidas do estado da campanha (para /carregar, /ficha, /mapa etc.).

Uso:
  python scripts/sessao.py resumo            briefing de início de sessão (Mestre)
  python scripts/sessao.py ficha             ficha do personagem
  python scripts/sessao.py mapa [local_id]   local atual (ou outro) e rotas
  python scripts/sessao.py magias [--escola fogo] [--rank iniciante] [--conhecidas]
  python scripts/sessao.py tecnicas [--escola deus_da_agua] [--conhecidas]
  python scripts/sessao.py inventario
  python scripts/sessao.py quests [--todas]
  python scripts/sessao.py faccoes [--mestre]  (sem --mestre mostra só o que é público)
  python scripts/sessao.py npc <id>            (Mestre)
  python scripts/sessao.py npcs [--local id] [--conhecidos]
  python scripts/sessao.py diario [n]          últimas n entradas (padrão 3)
"""
import argparse
import re

import rpgcomum as rc


def L(nome):
    return rc.ler(rc.camp(nome))


def locais():
    return rc.por_id(rc.ler(rc.DADOS / "locais.json")["locais"])


def entradas_diario(n):
    p = rc.CAMPANHA / "diario.md"
    if not p.exists():
        return []
    partes = re.split(r"(?m)^(?=## )", p.read_text(encoding="utf-8"))
    return [x.strip() for x in partes if x.startswith("## ")][-n:]


def ficha():
    p = L("personagem")
    if p.get("status_criacao") != "completo":
        print("Personagem ainda não criado.")
        return
    a = p["atributos"]
    print(f"{p['nome']} — {p['raca']}, {p['idade']} anos | origem: {p['origem']} | "
          f"{'Sem-Sonho' if p['sem_sonho'] else 'sonha'}")
    print("Atributos: " + "  ".join(f"{k[:3].upper()} {v:+d}" for k, v in a.items()))
    print(f"PV {p['pv']}/{p['pv_max']}  Mana {p['mana']}/{p['mana_max']}  "
          f"(crescimento de mana: {p['capacidade_mana_crescimento']})  "
          f"Encantação silenciosa: {'sim' if p['encantacao_silenciosa'] else 'não'}")
    mg = {k: v for k, v in p["ranks"]["magia"].items() if v != "nenhum"}
    es = {k: v for k, v in p["ranks"]["espada"].items() if v != "nenhum"}
    print("Ranks de magia: " + (", ".join(f"{k} {v}" for k, v in mg.items()) or "nenhum"))
    print("Ranks de espada: " + (", ".join(f"{k} {v}" for k, v in es.items()) or "nenhum"))
    print("Magias: " + (", ".join(p["magias_conhecidas"]) or "—"))
    print("Técnicas: " + (", ".join(p["tecnicas"]) or "—"))
    tr = p["tracos"]
    for k in ("bencaos", "maldicoes", "olhos_demoniacos", "outros"):
        if tr.get(k):
            print(f"{k.replace('_', ' ').capitalize()}: {', '.join(tr[k])}")
    if p["ferimentos_persistentes"]:
        print("Ferimentos: " + "; ".join(f"{f['descricao']} ({f['gravidade']})" for f in p["ferimentos_persistentes"]))
    print("Idiomas: " + ", ".join(p["idiomas"]))
    g = p["reputacao_guilda"]
    print(f"Guilda: rank {g['rank']} ({g['pontos']} pts) | Dinheiro: "
          + ", ".join(f"{v} {k}" for k, v in p["dinheiro"].items() if v))
    print("Objetivos: " + "; ".join(p["objetivos"]))
    if p["relacoes"]:
        npcs = rc.por_id(L("npcs")["npcs"])
        print("Relações: " + ", ".join(f"{npcs.get(k, {}).get('nome', k)} {v:+d}" for k, v in p["relacoes"].items()))
    if p["sonhos_registrados"]:
        s = p["sonhos_registrados"][-1]
        print(f"Último sonho ({s['data']}): {s['descricao']}")


def mapa(lid=None):
    e = L("estado")
    lc = locais()
    l = lc.get(lid or e["local_atual"])
    if not l:
        print("Local desconhecido.")
        return
    print(f"{l['nome']} — {l['continente']} / {l['regiao']} ({l['tipo']}), perigo {l['perigo']}/10")
    print(l["descricao"])
    print("Rotas:")
    for r in l["rotas"]:
        print(f"  → {lc[r['destino']]['nome']} [{r['destino']}]: {r['meio']}, {r['dias']} dias, perigo {r['perigo']}/10"
              + (f" — {r['notas']}" if r.get("notas") else ""))


def resumo():
    e = L("estado")
    lc = locais()
    print(f"== {rc.data_legivel(e['data_mundo'])} | {lc.get(e['local_atual'], {}).get('nome', e['local_atual'])} | clima: {e['clima']}")
    p = L("personagem")
    if p.get("status_criacao") == "completo":
        print(f"{p['nome']}: PV {p['pv']}/{p['pv_max']} Mana {p['mana']}/{p['mana_max']}"
              + (f" | ferimentos: {len(p['ferimentos_persistentes'])}" if p["ferimentos_persistentes"] else ""))
    else:
        print("Personagem: NÃO CRIADO (iniciar criação de personagem).")
    pt = L("party")
    npcs = rc.por_id(L("npcs")["npcs"])
    if pt["membros"]:
        print("Party: " + ", ".join(f"{npcs[m['npc_id']]['nome']} ({m['papel']})" for m in pt["membros"]))
    q = [x for x in L("quests")["quests"] if x["status"] == "ativa"]
    if q:
        print("Quests ativas: " + "; ".join(x["titulo"] for x in q))
    print("Relógios: " + ", ".join(f"{k} {v}/6" for k, v in e["relogios"].items()))
    if e["flags"]:
        print("Flags: " + ", ".join(e["flags"][-12:]))
    if e["noticias_recentes"]:
        print("Notícias recentes:")
        for n in e["noticias_recentes"][-5:]:
            print(f"  - [{n['data']}] {n['texto']}")
    arcos = rc.ler(rc.HISTORIA / "arcos.json")["arcos"]
    ativos = [a for a in arcos if a["status"] == "ativo"]
    if ativos:
        print("Arcos ativos (Mestre):")
        for a in ativos:
            fase = a["fases"][min(a.get("fase_atual", 0), len(a["fases"]) - 1)]
            print(f"  - {a['titulo']} [{a['id']}] fase {a.get('fase_atual', 0) + 1}/{len(a['fases'])}: {fase['objetivo']}")
    ent = entradas_diario(3)
    if ent:
        print("\nÚltimas entradas do diário:")
        for x in ent:
            print(x + "\n")


def magias(escola=None, rank=None, conhecidas=False):
    ms = rc.ler(rc.DADOS / "magias.json")["magias"]
    if conhecidas:
        k = set(L("personagem")["magias_conhecidas"])
        ms = [m for m in ms if m["id"] in k]
    ms = [m for m in ms if (not escola or m["escola"] == escola) and (not rank or m["rank"] == rank)]
    for m in ms:
        print(f"[{m['id']}] {m['nome']} — {m['escola']}/{m['rank']}, {m['custo_mana']} mana, {m['tempo_conjuracao']}, "
              f"{m['alcance']}{', dano ' + m['dano'] if m['dano'] else ''}{'' if m['pode_silenciosa'] else ', sem silenciosa'}")
        print(f"    {m['efeito']}")
    print(f"({len(ms)} magias)")


def tecnicas(escola=None, conhecidas=False):
    ts = rc.ler(rc.DADOS / "estilos_espada.json")["tecnicas"]
    if conhecidas:
        k = set(L("personagem")["tecnicas"])
        ts = [t for t in ts if t["id"] in k]
    for t in ts:
        if escola and t["escola"] != escola:
            continue
        print(f"[{t['id']}] {t['nome']} — {t['escola']}/{t['rank']}, custo: {t['custo']}")
        print(f"    {t['efeito']}")


def inventario():
    inv = L("inventario")
    it = rc.por_id(rc.ler(rc.DADOS / "itens.json")["itens"])
    for x in inv["itens"]:
        i = it.get(x["item_id"], {})
        print(f"- {x['qtd']}x {i.get('nome', x['item_id'])}{' (equipado)' if x.get('equipado') else ''}"
              + (f" — {x['notas']}" if x.get("notas") else ""))
    p = L("personagem")
    print("Dinheiro: " + (", ".join(f"{v} {k}" for k, v in p["dinheiro"].items() if v) or "nenhum"))


def quests(todas=False):
    for q in L("quests")["quests"]:
        if todas or q["status"] == "ativa":
            print(f"[{q['status']}] {q['titulo']} — {q['descricao']}")
            for o in q.get("objetivos", []):
                print(f"    {'[x]' if o['feito'] else '[ ]'} {o['texto']}")


def faccoes(mestre=False):
    for f in L("faccoes_estado")["faccoes"]:
        if not mestre and not f.get("conhecida_pelo_jogador", True):
            continue
        print(f"{f['nome']} ({f['tipo']}) — poder {f['poder']}/10, atitude {f['atitude_com_jogador']:+d}, {f['status']}")
        print("    Mostra: " + "; ".join(f["objetivos_publicos"]))
        if mestre:
            print("    Oculto: " + "; ".join(f["objetivos_ocultos"]))
            print("    Diante de um Sem-Sonho: " + f["postura_sem_sonho"])


def npc(i):
    n = rc.por_id(L("npcs")["npcs"]).get(i)
    if not n:
        print("NPC não encontrado.")
        return
    for k, v in n.items():
        print(f"{k}: {v}")


def npcs(local=None, conhecidos=False):
    for n in L("npcs")["npcs"]:
        if local and n["local_atual"] != local:
            continue
        if conhecidos and not n["conhecido_pelo_jogador"]:
            continue
        print(f"[{n['id']}] {n['nome']} — {n['raca']}, {n['status']}, em {n['local_atual']}")


def main():
    rc.utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--escola")
    ap.add_argument("--rank")
    ap.add_argument("--conhecidas", action="store_true")
    ap.add_argument("--conhecidos", action="store_true")
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("--mestre", action="store_true")
    ap.add_argument("--local")
    a = ap.parse_args()
    c = a.cmd
    if c == "resumo":
        resumo()
    elif c == "ficha":
        ficha()
    elif c == "mapa":
        mapa(a.arg)
    elif c == "magias":
        magias(a.escola, a.rank, a.conhecidas)
    elif c == "tecnicas":
        tecnicas(a.escola, a.conhecidas)
    elif c == "inventario":
        inventario()
    elif c == "quests":
        quests(a.todas)
    elif c == "faccoes":
        faccoes(a.mestre)
    elif c == "npc":
        npc(a.arg)
    elif c == "npcs":
        npcs(a.local, a.conhecidos)
    elif c == "diario":
        for x in entradas_diario(int(a.arg or 3)):
            print(x + "\n")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
