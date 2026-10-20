"""Edita campos dos arquivos de campanha/ (e status em historia/) por caminho pontuado, validando em seguida.

Uso:
  python scripts/editar.py <arquivo> get <caminho>
  python scripts/editar.py <arquivo> set <caminho> <valor>      valor em JSON ou texto
  python scripts/editar.py <arquivo> add <caminho> <número>     soma (ex.: pv -4)
  python scripts/editar.py <arquivo> push <caminho> <valor>     acrescenta à lista
  python scripts/editar.py <arquivo> pull <caminho> <valor>     remove da lista

<arquivo>: personagem, estado, party, npcs, faccoes_estado, quests, inventario,
           linha_do_tempo, arcos (os dois últimos em historia/).
Em listas de objetos, um segmento pode ser o id: npcs.maren_vossk.status
Exemplos:
  python scripts/editar.py personagem add pv -6
  python scripts/editar.py personagem set relacoes.maren_vossk 25
  python scripts/editar.py npcs set npcs.maren_vossk.conhecido_pelo_jogador true
  python scripts/editar.py estado push flags viu_primeiro_oco
  python scripts/editar.py arcos set arcos.a1_noite_dos_sinos.status ativo
"""
import json
import sys

import rpgcomum as rc
import validar

HIST = {"linha_do_tempo", "arcos"}
LIMITES = {"pv": "pv_max", "mana": "mana_max"}


def caminho_arquivo(nome):
    return (rc.HISTORIA if nome in HIST else rc.CAMPANHA) / f"{nome}.json"


def valor(txt):
    try:
        return json.loads(txt)
    except Exception:
        return txt


def descer(no, partes, criar=False):
    for p in partes:
        if isinstance(no, list):
            if p.isdigit():
                no = no[int(p)]
            else:
                achado = next((x for x in no if isinstance(x, dict) and x.get("id") == p), None)
                if achado is None:
                    raise SystemExit(f"id {p!r} não encontrado na lista")
                no = achado
        else:
            if p not in no:
                if not criar:
                    raise SystemExit(f"campo {p!r} não existe")
                no[p] = {}
            no = no[p]
    return no


def main():
    rc.utf8()
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    nome, op, cam = sys.argv[1], sys.argv[2], sys.argv[3]
    arg = sys.argv[4] if len(sys.argv) > 4 else None
    arq = caminho_arquivo(nome)
    doc = rc.ler(arq)
    partes = cam.split(".")
    if op == "get":
        print(json.dumps(descer(doc, partes), ensure_ascii=False, indent=2))
        return
    pai = descer(doc, partes[:-1], criar=True)
    chave = partes[-1]
    if isinstance(pai, list):
        raise SystemExit("O último segmento deve ser um campo, não um item de lista.")
    antes = pai.get(chave)
    if op == "set":
        pai[chave] = valor(arg)
    elif op == "add":
        novo = (antes or 0) + valor(arg)
        if chave in LIMITES and LIMITES[chave] in pai:
            novo = min(novo, pai[LIMITES[chave]])
        if isinstance(antes, int) and chave in ("atitude", "atitude_com_jogador") or cam.startswith("relacoes."):
            novo = max(-100, min(100, novo))
        pai[chave] = novo
    elif op == "push":
        pai.setdefault(chave, []).append(valor(arg))
    elif op == "pull":
        v = valor(arg)
        if v in pai.get(chave, []):
            pai[chave].remove(v)
        else:
            raise SystemExit(f"{v!r} não está em {cam}")
    else:
        raise SystemExit(f"Operação inválida: {op}")
    rc.gravar(arq, doc)
    sens = nome == "segredos"
    print(f"{nome}.{cam}: {'(oculto)' if sens else json.dumps(antes, ensure_ascii=False)} → "
          f"{'(oculto)' if sens else json.dumps(pai[chave], ensure_ascii=False)}")
    if not validar.executar(silencioso=True):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
