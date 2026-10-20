"""Snapshots de campanha/ (e dos arquivos de historia/ que mudam durante o jogo).

Uso:
  python scripts/backup.py [--nome rotulo]     cria backups/AAAA-MM-DD_HHMM[_rotulo]/
  python scripts/backup.py --listar
  python scripts/backup.py --restaurar <pasta> restaura um backup (faz backup do estado atual antes)
  python scripts/backup.py --resetar           volta ao mundo inicial (modelos/campanha_inicial)
  python scripts/backup.py --gravar-modelo     grava o estado atual como mundo inicial (só na construção)

historia/linha_do_tempo.json, arcos.json e segredos.json mudam de status durante o jogo,
por isso entram no snapshot (subpasta historia/).
"""
import argparse
import re
import shutil
from datetime import datetime

import rpgcomum as rc

HISTORIA_MUTAVEL = ["linha_do_tempo.json", "arcos.json", "segredos.json"]


def copiar_estado(destino):
    destino.mkdir(parents=True)
    for f in rc.CAMPANHA.iterdir():
        if f.is_file():
            shutil.copy2(f, destino / f.name)
    (destino / "historia").mkdir()
    for nome in HISTORIA_MUTAVEL:
        if (rc.HISTORIA / nome).exists():
            shutil.copy2(rc.HISTORIA / nome, destino / "historia" / nome)


def criar(rotulo=None):
    rc.BACKUPS.mkdir(exist_ok=True)
    base = f"{datetime.now():%Y-%m-%d_%H%M}"
    if rotulo:
        base += "_" + re.sub(r"[^a-z0-9_-]+", "_", rotulo.lower()).strip("_")
    destino, i = rc.BACKUPS / base, 2
    while destino.exists():
        destino = rc.BACKUPS / f"{base}-{i}"
        i += 1
    copiar_estado(destino)
    return destino


def restaurar_de(origem):
    for f in rc.CAMPANHA.iterdir():
        if f.is_file():
            f.unlink()
    for f in origem.iterdir():
        if f.is_file():
            shutil.copy2(f, rc.CAMPANHA / f.name)
    hist = origem / "historia"
    if hist.is_dir():
        for nome in HISTORIA_MUTAVEL:
            if (hist / nome).exists():
                shutil.copy2(hist / nome, rc.HISTORIA / nome)


def main():
    rc.utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--nome")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--restaurar")
    ap.add_argument("--resetar", action="store_true")
    ap.add_argument("--gravar-modelo", action="store_true")
    a = ap.parse_args()

    if a.listar:
        pastas = sorted(p.name for p in rc.BACKUPS.iterdir() if p.is_dir()) if rc.BACKUPS.exists() else []
        print("\n".join(pastas) if pastas else "Nenhum backup.")
        return
    if a.gravar_modelo:
        if rc.MODELO_INICIAL.exists():
            shutil.rmtree(rc.MODELO_INICIAL)
        copiar_estado(rc.MODELO_INICIAL)
        log = rc.MODELO_INICIAL / "rolagens.log"
        if log.exists():
            log.unlink()
        print(f"Modelo inicial gravado em {rc.MODELO_INICIAL.relative_to(rc.RAIZ).as_posix()}")
        return
    if a.restaurar or a.resetar:
        origem = rc.MODELO_INICIAL if a.resetar else rc.BACKUPS / a.restaurar
        if not origem.is_dir():
            raise SystemExit(f"Não encontrado: {origem}")
        seguranca = criar("antes_de_restaurar")
        restaurar_de(origem)
        print(f"Estado restaurado de {origem.relative_to(rc.RAIZ).as_posix()} "
              f"(estado anterior salvo em backups/{seguranca.name})")
        return
    d = criar(a.nome)
    print(f"Backup criado: backups/{d.name}")


if __name__ == "__main__":
    main()
