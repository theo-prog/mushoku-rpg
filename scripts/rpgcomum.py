"""Utilidades compartilhadas pelos scripts da campanha "O Ano Sem Sonhos"."""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMPANHA = RAIZ / "campanha"
DADOS = RAIZ / "dados"
HISTORIA = RAIZ / "historia"
SCHEMAS = RAIZ / "schemas"
BACKUPS = RAIZ / "backups"
MODELO_INICIAL = RAIZ / "modelos" / "campanha_inicial"

# Calendário do Dragão Blindado (desta realidade: 12 meses de 30 dias).
DIAS_MES = 30
MESES = 12
NOMES_MESES = [
    "Degelo", "Semeadura", "Chuvas", "Florada", "Verdor", "Sol-Alto",
    "Colheita", "Ventos", "Brumas", "Geada", "Longa-Noite", "Vigília",
]
DATA_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

RANKS = ["nenhum", "iniciante", "intermediario", "avancado", "santo", "rei", "imperador", "deus"]
RANK_BONUS = {"nenhum": 0, "iniciante": 1, "intermediario": 2, "avancado": 4,
              "santo": 6, "rei": 9, "imperador": 12, "deus": 15}
ATRIBUTOS = ["forca", "agilidade", "vigor", "intelecto", "percepcao", "presenca"]
RELOGIOS = ["descida", "coroa_silenciosa", "purificacao", "titulo_vago", "migracao"]


def utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def ler(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def gravar(caminho, obj):
    Path(caminho).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def camp(nome):
    return CAMPANHA / f"{nome}.json"


def data_para_dias(s):
    m = DATA_RE.match(s or "")
    if not m:
        raise ValueError(f"data inválida: {s!r} (use AAAA-MM-DD)")
    a, me, d = map(int, m.groups())
    if not (1 <= me <= MESES and 1 <= d <= DIAS_MES):
        raise ValueError(f"data fora do calendário: {s!r}")
    return (a * MESES + (me - 1)) * DIAS_MES + (d - 1)


def dias_para_data(n):
    a, r = divmod(n, MESES * DIAS_MES)
    me, d = divmod(r, DIAS_MES)
    return f"{a:04d}-{me + 1:02d}-{d + 1:02d}"


def data_completa(s):
    return bool(DATA_RE.match(s or ""))


def data_legivel(s):
    m = DATA_RE.match(s or "")
    if not m:
        return s
    a, me, d = map(int, m.groups())
    return f"{d} de {NOMES_MESES[me - 1]} do ano {a} (C.D.B.)"


def idade_em(nascimento, hoje):
    if not (data_completa(nascimento) and data_completa(hoje)):
        return None
    return (data_para_dias(hoje) - data_para_dias(nascimento)) // (MESES * DIAS_MES)


def por_id(lista):
    return {x["id"]: x for x in lista if isinstance(x, dict) and "id" in x}
