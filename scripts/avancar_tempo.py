"""Avança a data do mundo e dispara eventos da linha do tempo (os relógios andam sem o jogador).

Uso:
  python scripts/avancar_tempo.py 30                      avança 30 dias
  python scripts/avancar_tempo.py --ate 0423-06-14        avança até a data
  python scripts/avancar_tempo.py --viagem sharia         usa a rota a partir do local atual (dias da rota)
  python scripts/avancar_tempo.py 7 --descanso            descanso: recupera mana e PV (regras/sistema.md)
  python scripts/avancar_tempo.py 30 --simular            mostra o que aconteceria, sem gravar

Saída voltada ao Mestre: eventos disparados, notícias públicas e lembretes de sonhos.
"""
import argparse

import rpgcomum as rc
import validar


def aplicar_efeitos(ev, estado, npcs, fac, log):
    N = rc.por_id(npcs)
    F = rc.por_id(fac)
    for ef in ev.get("efeitos", []):
        t = ef.get("tipo")
        if t == "flag":
            if ef["valor"] not in estado["flags"]:
                estado["flags"].append(ef["valor"])
        elif t == "remover_flag":
            if ef["valor"] in estado["flags"]:
                estado["flags"].remove(ef["valor"])
        elif t == "npc_status" and ef.get("npc_id") in N:
            N[ef["npc_id"]]["status"] = ef["status"]
            if ef["status"] == "oco":
                N[ef["npc_id"]]["oco"] = True
        elif t == "npc_local" and ef.get("npc_id") in N:
            N[ef["npc_id"]]["local_atual"] = ef["local_id"]
        elif t == "faccao_poder" and ef.get("faccao_id") in F:
            f = F[ef["faccao_id"]]
            f["poder"] = max(0, min(10, f["poder"] + ef["delta"]))
        elif t == "faccao_atitude" and ef.get("faccao_id") in F:
            f = F[ef["faccao_id"]]
            f["atitude_com_jogador"] = max(-100, min(100, f["atitude_com_jogador"] + ef["delta"]))
        elif t == "faccao_status" and ef.get("faccao_id") in F:
            F[ef["faccao_id"]]["status"] = ef["status"]
        else:
            log.append(f"    (efeito não aplicado automaticamente: {ef})")
            continue
        log.append(f"    efeito: {t} {ef.get('npc_id') or ef.get('faccao_id') or ef.get('valor')}")


def main():
    rc.utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("dias", nargs="?", type=int)
    ap.add_argument("--ate")
    ap.add_argument("--viagem")
    ap.add_argument("--descanso", action="store_true")
    ap.add_argument("--simular", action="store_true")
    a = ap.parse_args()

    estado = rc.ler(rc.camp("estado"))
    tl_doc = rc.ler(rc.HISTORIA / "linha_do_tempo.json")
    npcs_doc = rc.ler(rc.camp("npcs"))
    fac_doc = rc.ler(rc.camp("faccoes_estado"))
    pers = rc.ler(rc.camp("personagem"))
    locais = rc.por_id(rc.ler(rc.DADOS / "locais.json")["locais"])

    hoje = rc.data_para_dias(estado["data_mundo"])
    dias = a.dias or 0
    destino_viagem = None
    if a.viagem:
        origem = locais.get(estado.get("local_atual"))
        rota = next((r for r in (origem or {}).get("rotas", []) if r["destino"] == a.viagem), None)
        if not rota:
            opcoes = ", ".join(f"{r['destino']} ({r['dias']}d)" for r in (origem or {}).get("rotas", []))
            raise SystemExit(f"Sem rota direta de {estado.get('local_atual')} para {a.viagem}. Rotas: {opcoes}")
        dias = dias or rota["dias"]
        destino_viagem = a.viagem
        print(f"Viagem {origem['nome']} → {locais[a.viagem]['nome']}: {rota['meio']}, {dias} dias, perigo {rota['perigo']}/10")
    if a.ate:
        dias = rc.data_para_dias(a.ate) - hoje
    if dias <= 0:
        raise SystemExit("Nada a avançar (informe dias > 0, --ate futura ou --viagem).")

    novo = hoje + dias
    estado["data_mundo"] = rc.dias_para_data(novo)
    if destino_viagem:
        estado["local_atual"] = destino_viagem

    statuses = {e["id"]: e["status"] for e in tl_doc["eventos"]}
    pendentes = sorted(
        (e for e in tl_doc["eventos"]
         if e["status"] == "futuro" and rc.data_completa(e["data_mundo"]) and rc.data_para_dias(e["data_mundo"]) <= novo),
        key=lambda e: e["data_mundo"])
    log, disparados, revisar = [], [], []
    for ev in pendentes:
        bloqueio = [d for d in ev.get("depende_de", []) if statuses.get(d) in ("evitado", "alterado")]
        if bloqueio:
            revisar.append(f"  ! {ev['id']} depende de {bloqueio} (evitado/alterado): o Mestre decide se ocorre, muda ou é evitado.")
            continue
        ev["status"] = "ocorrido"
        statuses[ev["id"]] = "ocorrido"
        if ev.get("relogio_id"):
            estado["relogios"][ev["relogio_id"]] = max(estado["relogios"].get(ev["relogio_id"], 0), ev.get("estagio", 0))
        if ev.get("noticia_publica"):
            estado["noticias_recentes"].append({
                "data": ev["data_mundo"], "evento_id": ev["id"],
                "local_id": ev.get("local_id"), "texto": ev["noticia_publica"]})
        disparados.append(ev)
        log.append(f"  * [{ev['data_mundo']}] {ev['titulo']} (relógio {ev.get('relogio_id')} → estágio {ev.get('estagio')})")
        log.append(f"    {ev['descricao']}")
        for c in ev.get("consequencias", []):
            log.append(f"    → {c}")
        aplicar_efeitos(ev, estado, npcs_doc["npcs"], fac_doc["faccoes"], log)
    estado["noticias_recentes"] = estado["noticias_recentes"][-15:]

    idade = rc.idade_em(pers.get("data_nascimento_mundo", ""), estado["data_mundo"])
    if idade is not None and idade != pers.get("idade"):
        log.append(f"  Aniversário: o personagem agora tem {idade} anos.")
        pers["idade"] = idade
    if a.descanso:
        vig = int(pers.get("atributos", {}).get("vigor", 0))
        cura = dias * max(1, 2 + vig)
        pers["pv"] = min(pers["pv_max"], pers["pv"] + cura)
        pers["mana"] = pers["mana_max"]
        log.append(f"  Descanso: PV {pers['pv']}/{pers['pv_max']} (+{cura}), mana {pers['mana']}/{pers['mana_max']}. "
                   "Ferimentos persistentes não somem com descanso.")

    print(f"Tempo: {rc.data_legivel(rc.dias_para_data(hoje))} → {rc.data_legivel(estado['data_mundo'])} (+{dias} dias)")
    print(f"Eventos disparados: {len(disparados)}")
    print("\n".join(log) if log else "  (nenhum)")
    if revisar:
        print("Revisar:")
        print("\n".join(revisar))
    print(f"Lembrete: {dias} noite(s) passaram. Narre sonhos (ou a ausência deles) e registre em sonhos_registrados; "
          "considere quem vigiou o sono.")
    proximos = sorted((e for e in tl_doc["eventos"] if e["status"] == "futuro" and rc.data_completa(e["data_mundo"])),
                      key=lambda e: e["data_mundo"])[:3]
    if proximos:
        print("Próximos no horizonte: " + "; ".join(f"{e['data_mundo']} {e['titulo']}" for e in proximos))

    if a.simular:
        print("(simulação: nada gravado)")
        return
    rc.gravar(rc.camp("estado"), estado)
    rc.gravar(rc.HISTORIA / "linha_do_tempo.json", tl_doc)
    rc.gravar(rc.camp("npcs"), npcs_doc)
    rc.gravar(rc.camp("faccoes_estado"), fac_doc)
    rc.gravar(rc.camp("personagem"), pers)
    if not validar.executar(silencioso=True):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
