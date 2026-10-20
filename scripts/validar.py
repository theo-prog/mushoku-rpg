"""Valida todos os JSON de dados/, historia/ e campanha/ contra schemas/ e checa referências cruzadas.

Uso:
  python scripts/validar.py              (valida tudo; código de saída 1 se houver erro)
  python scripts/validar.py --modelo     (valida também modelos/campanha_inicial)
  python scripts/validar.py --silencioso (só imprime erros)

Arquivos sensíveis (historia/segredos.json) nunca têm valores impressos: só o caminho do erro.
"""
import argparse
import re
import sys
from pathlib import Path

import rpgcomum as rc

SENSIVEIS = {"segredos.json"}
TIPOS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def resolver(raiz, ref):
    if not ref.startswith("#/"):
        raise ValueError(f"$ref não suportado: {ref}")
    no = raiz
    for parte in ref[2:].split("/"):
        no = no[parte]
    return no


def validar(v, s, raiz, cam, erros, sens):
    def erro(msg, valor=None):
        detalhe = "" if sens or valor is None else f" (valor: {str(valor)[:60]!r})"
        erros.append(f"{cam or '<raiz>'}: {msg}{detalhe}")

    if "$ref" in s:
        s = resolver(raiz, s["$ref"])
    if "anyOf" in s:
        if not any(not _sub(v, x, raiz, cam) for x in s["anyOf"]):
            erro("não corresponde a nenhuma alternativa (anyOf)", v)
        return
    t = s.get("type")
    if t:
        tipos = t if isinstance(t, list) else [t]
        if not any(TIPOS[x](v) for x in tipos):
            erro(f"tipo esperado {t}", v)
            return
    if "enum" in s and v not in s["enum"]:
        erro(f"valor fora de {s['enum']}" if not sens else "valor fora do enum", v)
    if "const" in s and v != s["const"]:
        erro("valor diferente do esperado", v)
    if TIPOS["number"](v):
        if "minimum" in s and v < s["minimum"]:
            erro(f"menor que {s['minimum']}", v)
        if "maximum" in s and v > s["maximum"]:
            erro(f"maior que {s['maximum']}", v)
    if isinstance(v, str):
        if "minLength" in s and len(v) < s["minLength"]:
            erro(f"texto menor que {s['minLength']}", v)
        if "pattern" in s and not re.search(s["pattern"], v):
            erro(f"não casa com o padrão {s['pattern']}", v)
    if isinstance(v, list):
        if "minItems" in s and len(v) < s["minItems"]:
            erro(f"precisa de ao menos {s['minItems']} itens (tem {len(v)})")
        if s.get("uniqueItems"):
            vistos = [repr(x) for x in v]
            if len(set(vistos)) != len(vistos):
                erro("itens repetidos")
        if "items" in s:
            for i, x in enumerate(v):
                validar(x, s["items"], raiz, f"{cam}[{i}]", erros, sens)
    if isinstance(v, dict):
        for r in s.get("required", []):
            if r not in v:
                erro(f"campo obrigatório ausente: {r}")
        props = s.get("properties", {})
        adic = s.get("additionalProperties", True)
        pn = s.get("propertyNames")
        for k, x in v.items():
            if pn and "pattern" in pn and not re.search(pn["pattern"], k):
                erro(f"nome de chave inválido: {k!r}")
            if k in props:
                validar(x, props[k], raiz, f"{cam}.{k}" if cam else k, erros, sens)
            elif adic is False:
                erro(f"campo não previsto: {k}")
            elif isinstance(adic, dict):
                validar(x, adic, raiz, f"{cam}.{k}" if cam else k, erros, sens)


def _sub(v, s, raiz, cam):
    e = []
    validar(v, s, raiz, cam, e, True)
    return e


def ids_unicos(lista, nome, erros):
    vistos = set()
    for x in lista:
        i = x.get("id") if isinstance(x, dict) else None
        if i in vistos:
            erros.append(f"{nome}: id duplicado {i!r}")
        vistos.add(i)
    return vistos


def carregar_seguro(p):
    try:
        return rc.ler(p)
    except Exception:
        return None


def checar_referencias(base_camp, erros):
    D = lambda n: carregar_seguro(rc.DADOS / f"{n}.json") or {}
    H = lambda n: carregar_seguro(rc.HISTORIA / f"{n}.json") or {}
    C = lambda n: carregar_seguro(base_camp / f"{n}.json") or {}

    magias = D("magias").get("magias", [])
    estilos = D("estilos_espada").get("tecnicas", [])
    racas = D("racas").get("racas", [])
    itens = D("itens").get("itens", [])
    monstros = D("monstros").get("monstros", [])
    locais = D("locais").get("locais", [])
    tl = H("linha_do_tempo").get("eventos", [])
    arcos = H("arcos").get("arcos", [])
    seg = H("segredos")
    npcs = C("npcs").get("npcs", [])
    fac = C("faccoes_estado").get("faccoes", [])
    quests = C("quests").get("quests", [])

    I = {}
    for nome, lst in [("magias", magias), ("tecnicas", estilos), ("racas", racas), ("itens", itens),
                      ("monstros", monstros), ("locais", locais), ("eventos", tl), ("arcos", arcos),
                      ("npcs", npcs), ("faccoes", fac), ("quests", quests)]:
        I[nome] = ids_unicos(lst, nome, erros)
    revel = {r.get("id") for r in seg.get("revelacoes", []) if isinstance(r, dict)}

    def ref(origem, valor, conj, nome, opcional=False):
        if valor in (None, "") and opcional:
            return
        if valor not in I.get(conj, conj if isinstance(conj, set) else set()):
            erros.append(f"{origem}: referência inexistente a {nome} {valor!r}")

    for l in locais:
        for r in l.get("rotas", []):
            ref(f"locais.{l['id']}.rotas", r.get("destino"), "locais", "local")
        ref(f"locais.{l['id']}", l.get("faccao_controle"), "faccoes", "facção", True)
    for n in npcs:
        ref(f"npcs.{n['id']}", n.get("faccao_id"), "faccoes", "facção", True)
        ref(f"npcs.{n['id']}", n.get("local_atual"), "locais", "local", True)
        ref(f"npcs.{n['id']}", n.get("raca"), "racas", "raça")
    for f in fac:
        ref(f"faccoes.{f['id']}", f.get("lider_npc_id"), "npcs", "npc", True)
        ref(f"faccoes.{f['id']}", f.get("sede_local_id"), "locais", "local", True)
        for k in f.get("relacoes", {}):
            ref(f"faccoes.{f['id']}.relacoes", k, "faccoes", "facção")
    for e in tl:
        ref(f"linha_do_tempo.{e['id']}", e.get("local_id"), "locais", "local", True)
        for x in e.get("faccoes_envolvidas", []):
            ref(f"linha_do_tempo.{e['id']}", x, "faccoes", "facção")
        for x in e.get("depende_de", []):
            ref(f"linha_do_tempo.{e['id']}.depende_de", x, "eventos", "evento")
        for ef in e.get("efeitos", []):
            if "npc_id" in ef:
                ref(f"linha_do_tempo.{e['id']}.efeitos", ef["npc_id"], "npcs", "npc")
            if "faccao_id" in ef:
                ref(f"linha_do_tempo.{e['id']}.efeitos", ef["faccao_id"], "faccoes", "facção")
            if "local_id" in ef:
                ref(f"linha_do_tempo.{e['id']}.efeitos", ef["local_id"], "locais", "local")
    for a in arcos:
        for x in a.get("npcs_chave", []):
            ref(f"arcos.{a['id']}", x, "npcs", "npc")
        for p in a.get("pistas", []):
            ref(f"arcos.{a['id']}.pistas", p.get("local_id"), "locais", "local")
            if revel and p.get("revelacao_id") not in revel:
                erros.append(f"arcos.{a['id']}.pistas: revelacao_id inexistente em segredos.json")
    if revel:
        contagem = {}
        for a in arcos:
            for p in a.get("pistas", []):
                contagem.setdefault(p.get("revelacao_id"), set()).add(p.get("local_id"))
        ordem = [x.get("id") for x in seg.get("revelacoes", []) if isinstance(x, dict)]
        for n, r in enumerate(ordem, 1):
            if len(contagem.get(r, ())) < 3:
                erros.append(f"regra das 3 pistas: revelação nº {n} de segredos.json tem pistas em só "
                             f"{len(contagem.get(r, ()))} local(is) (id oculto; confira em silêncio)")
    for m in monstros:
        for x in m.get("locais", []):
            ref(f"monstros.{m['id']}", x, "locais", "local")
    for t in estilos:
        for x in t.get("requisitos_tecnicas", []):
            ref(f"tecnicas.{t['id']}", x, "tecnicas", "técnica")

    p = C("personagem")
    if p:
        for x in p.get("magias_conhecidas", []):
            ref("personagem.magias_conhecidas", x, "magias", "magia")
        for x in p.get("tecnicas", []):
            ref("personagem.tecnicas", x, "tecnicas", "técnica")
        for k in p.get("relacoes", {}):
            ref("personagem.relacoes", k, "npcs", "npc")
        if p.get("raca"):
            ref("personagem", p.get("raca"), "racas", "raça")
    for m in C("party").get("membros", []):
        ref("party.membros", m.get("npc_id"), "npcs", "npc")
    for it in C("inventario").get("itens", []):
        ref("inventario.itens", it.get("item_id"), "itens", "item")
    for q in quests:
        ref(f"quests.{q['id']}", q.get("npc_origem"), "npcs", "npc", True)
        ref(f"quests.{q['id']}", q.get("local_id"), "locais", "local", True)
        ref(f"quests.{q['id']}", q.get("arco_id"), "arcos", "arco", True)
    est = C("estado")
    if est:
        ref("estado.local_atual", est.get("local_atual"), "locais", "local", True)


def arquivos(incluir_modelo):
    pastas = [rc.DADOS, rc.HISTORIA, rc.CAMPANHA]
    if incluir_modelo:
        pastas.append(rc.MODELO_INICIAL)
    for pasta in pastas:
        for f in sorted(pasta.glob("*.json")):
            yield f


def executar(incluir_modelo=False, silencioso=False):
    erros = []
    n = 0
    for f in arquivos(incluir_modelo):
        sens = f.name in SENSIVEIS
        sch_path = rc.SCHEMAS / f"{f.stem}.schema.json"
        rel = f.relative_to(rc.RAIZ).as_posix()
        if not sch_path.exists():
            erros.append(f"{rel}: sem schema em schemas/{f.stem}.schema.json")
            continue
        try:
            inst = rc.ler(f)
        except Exception as e:
            erros.append(f"{rel}: JSON inválido ({'detalhe oculto' if sens else e})")
            continue
        sch = rc.ler(sch_path)
        e = []
        validar(inst, sch, sch, "", e, sens)
        erros += [f"{rel}: {x}" for x in e]
        n += 1
    checar_referencias(rc.CAMPANHA, erros)
    if incluir_modelo and rc.MODELO_INICIAL.exists():
        checar_referencias(rc.MODELO_INICIAL, erros)
    if erros:
        print(f"VALIDAÇÃO FALHOU: {len(erros)} erro(s) em {n} arquivo(s).")
        for x in erros[:200]:
            print("  -", x)
        return False
    if not silencioso:
        print(f"Validação OK: {n} arquivos JSON conferidos (schemas + referências cruzadas).")
    return True


def main():
    rc.utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", action="store_true")
    ap.add_argument("--silencioso", action="store_true")
    a = ap.parse_args()
    sys.exit(0 if executar(a.modelo, a.silencioso) else 1)


if __name__ == "__main__":
    main()
