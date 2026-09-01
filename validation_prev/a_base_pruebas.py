import json
import random
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("../data/voting_docs_enriched.json")

with DATA_FILE.open(encoding="utf-8") as f:
    records = json.load(f)
assert isinstance(records, list)

# Testset original: se usa para EXCLUIR los datos ya seleccionados alli,
# de modo que esta carpeta genere un testset distinto (sin solapamiento).
ORIGINAL_TESTSET_FILE = Path("../validation/testset/preguntas_contexto_esperado.json")

MESES_ES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]

# Configuración global - Variables por categoría
MAX_FECHA = 10  # Máximo preguntas por fecha específica
MAX_ASUNTO = 40  # Máximo preguntas por asunto
MAX_PRESIDENTE = 10  # Máximo preguntas por presidente

# Semillas para reproducibilidad (distintas a las del testset original)
SEMILLA_FECHA = 137
SEMILLA_ASUNTO = 137
SEMILLA_PRESIDENTE = 137


def human_date_es(iso_date: str) -> str:
    dt = datetime.fromisoformat(iso_date)
    return f"{dt.day} de {MESES_ES[dt.month - 1]} de {dt.year}"


def format_document_context(record: dict) -> str:
    """Formatea un documento con el mismo formato usado en la indexación de Qdrant"""
    return (
        f"Votación del {record.get('fecha_larga')}.\n"
        f"Legislatura: {record.get('legislatura')} – Congreso {record.get('periodo_congreso')}.\n"
        f"Periodo anual: {record.get('periodo_anual')}.\n"
        f"Asunto: {record.get('asunto')}.\n"
        f"Presidente de la sesión: {record.get('presidente')}.\n"
        f"URL: {record.get('url')}"
    )


# Diccionario principal para todas las categorías
all_queries = {}

####################################################
# === EXCLUSIONES: datos ya usados en el testset original ===
####################################################
url_to_record = {r["url"]: r for r in records}

fechas_usadas: set[str] = set()
asuntos_usados: set[str] = set()
presidentes_usados: set[str] = set()

if ORIGINAL_TESTSET_FILE.exists():
    original = json.loads(ORIGINAL_TESTSET_FILE.read_text(encoding="utf-8"))

    for item in original.get("fecha", []):
        for ctx in item.get("context", []):
            m = re.search(r"URL:\s*(\S+)", ctx)
            if m and m.group(1) in url_to_record:
                fechas_usadas.add(url_to_record[m.group(1)]["fecha_ddmmyyyy"])

    for item in original.get("asunto", []):
        m = re.search(r"asunto '(.+)'\?$", item["query"])
        if m:
            asuntos_usados.add(m.group(1))

    for item in original.get("presidente", []):
        m = re.search(r"cuando (.+) presidió la sesión\?$", item["query"])
        if m:
            presidentes_usados.add(m.group(1))

    print(
        f"⚠️  Excluyendo datos del testset original: "
        f"{len(fechas_usadas)} fechas, {len(asuntos_usados)} asuntos, "
        f"{len(presidentes_usados)} presidentes"
    )
else:
    print(f"⚠️  No se encontró el testset original en {ORIGINAL_TESTSET_FILE}; no se excluye nada")

####################################################
# === 1. Por FECHA específica ===
####################################################
# Agrupar por fecha para incluir todas las votaciones del mismo día
fecha_map = defaultdict(list)
for r in records:
    fecha_key = r["fecha_ddmmyyyy"]  # Usar la fecha del día completo como clave
    fecha_map[fecha_key].append(r)

fechas_disponibles = [item for item in fecha_map.items() if item[0] not in fechas_usadas]
random.seed(SEMILLA_FECHA)
random.shuffle(fechas_disponibles)
out_fecha = []
for fecha_ddmmyyyy, records_fecha in fechas_disponibles[:MAX_FECHA]:
    # Usar el primer registro para obtener la fecha_utc5 para el formato humano
    fecha_utc5_sample = records_fecha[0]["fecha_utc5"]
    pregunta = f"¿Cuáles fueron las votaciones del Congreso el {human_date_es(fecha_utc5_sample)}?"
    context = [format_document_context(rec) for rec in records_fecha]
    out_fecha.append({"query": pregunta, "context": context})
all_queries["fecha"] = out_fecha

####################################################
# === 2. Por ASUNTO ===
####################################################
asunto_map = defaultdict(list)
for r in records:
    if r.get("asunto"):  # Solo incluir registros que tengan asunto
        asunto_map[r["asunto"]].append(r)

asuntos_disponibles = [item for item in asunto_map.items() if item[0] not in asuntos_usados]
random.seed(SEMILLA_ASUNTO)
random.shuffle(asuntos_disponibles)
out_asunto = []
for asunto, records_asunto in asuntos_disponibles[:MAX_ASUNTO]:
    pregunta = f"¿Qué días se trataron las votaciones con asunto '{asunto}'?"
    context = [format_document_context(rec) for rec in records_asunto]
    out_asunto.append({"query": pregunta, "context": context})
all_queries["asunto"] = out_asunto

####################################################
# === 3. Por PRESIDENTE ===
####################################################
presidente_map = defaultdict(list)
for r in records:
    if r.get("presidente"):  # Solo incluir registros que tengan presidente
        presidente_map[r["presidente"]].append(r)

presidentes_disponibles = [
    item for item in presidente_map.items() if item[0] not in presidentes_usados
]
random.seed(SEMILLA_PRESIDENTE)
random.shuffle(presidentes_disponibles)
out_presidente = []
for presidente, records_presidente in presidentes_disponibles[:MAX_PRESIDENTE]:
    # Tomar una muestra aleatoria de sesiones para este presidente
    sample_records = random.sample(records_presidente, min(3, len(records_presidente)))
    for rec in sample_records:
        pregunta = f"¿Qué votaciones se realizaron el día {human_date_es(rec['fecha_utc5'])} cuando {presidente} presidió la sesión?"
        context = [format_document_context(rec)]
        out_presidente.append({"query": pregunta, "context": context})
        if len(out_presidente) >= MAX_PRESIDENTE:
            break
    if len(out_presidente) >= MAX_PRESIDENTE:
        break
all_queries["presidente"] = out_presidente


####################################################
# === GUARDAR ARCHIVO ÚNICO ===
####################################################
output_file = Path("./testset/preguntas_contexto_esperado.json")
output_file.parent.mkdir(exist_ok=True)
output_file.write_text(json.dumps(all_queries, ensure_ascii=False, indent=2), encoding="utf-8")

# Estadísticas
print("✅ Generadas bases de prueba para 3 categorías:")
for categoria, queries in all_queries.items():
    print(f"  - {categoria}: {len(queries)} preguntas")

print(f"\n📁 Archivo generado: {output_file}")
print(f"📊 Total de preguntas: {sum(len(queries) for queries in all_queries.values())}")

# Mostrar ejemplo de estructura
print("\n📋 Estructura del JSON generado:")
for categoria in all_queries.keys():
    print(f"  - {categoria}")
    if all_queries[categoria]:
        ejemplo = all_queries[categoria][0]
        print(f"    Ejemplo: {ejemplo['query'][:60]}...")

print(f"\n🔍 Estadísticas de agrupación:")
print(f"  - Fechas distintas: {len(fecha_map)}")
print(f"  - Asuntos distintos: {len(asunto_map)}")
print(f"  - Presidentes distintos: {len(presidente_map)}")
print(f"  - Total de documentos: {len(records)}")
print(f"\n⚙️  Configuración:")
print(f"  - MAX_FECHA = {MAX_FECHA} (semilla: {SEMILLA_FECHA})")
print(f"  - MAX_ASUNTO = {MAX_ASUNTO} (semilla: {SEMILLA_ASUNTO})")
print(f"  - MAX_PRESIDENTE = {MAX_PRESIDENTE} (semilla: {SEMILLA_PRESIDENTE})")
