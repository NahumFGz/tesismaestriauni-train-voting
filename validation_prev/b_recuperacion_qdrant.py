# ## 1. Seleccionar base de pruebas
import json

# Leer el archivo de preguntas y contextos esperados
with open("./testset/preguntas_contexto_esperado.json", encoding="utf-8") as f:
    preguntas_contexto = json.load(f)

# Extraer los tipos (por ejemplo: "fecha", "mes", "legislatura")
tipos_disponibles = list(preguntas_contexto.keys())

# Crear un diccionario con las preguntas por tipo
preguntas_por_tipo = {}
for tipo in tipos_disponibles:
    preguntas_por_tipo[tipo] = [item["query"] for item in preguntas_contexto[tipo]]

# Ahora tienes:
# - tipos_disponibles: lista de los tipos (['fecha', ...])
# - preguntas_por_tipo: diccionario {tipo: [pregunta1, pregunta2, ...]}

# Ejemplo de impresión para verificar
for tipo in tipos_disponibles:
    print(f"Tipo: {tipo} ({len(preguntas_por_tipo[tipo])} preguntas)")
    for pregunta in preguntas_por_tipo[tipo][
        :3
    ]:  # Muestra solo las primeras 3 preguntas de cada tipo
        print("  -", pregunta)
    print()

# ## 2. Recuperar con y generar contextos con ***qdrant***

import asyncio
import json
import os
import sys

# Asegura la ruta al módulo
sys.path.append("/home/naflg/GithubProjects/tesismaestriauni-launcher/train-voting/tools")

from main_retriever import consultar_votacion  # type: ignore

INPUT_FILE = "./testset/preguntas_contexto_esperado.json"
OUTPUT_DIR = "./testset"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "contexto_qdrant.json")

# Carga preguntas por tipo
with open(INPUT_FILE, encoding="utf-8") as f:
    preguntas_contexto = json.load(f)

tipos_disponibles = list(preguntas_contexto.keys())


async def construir_contexto_qdrant(modo: str = "all", sample_size: int = 2):
    """
    Construye y guarda el JSON en el formato deseado.
    - modo="sample": procesa solo `sample_size` preguntas por tipo.
    - modo="all": procesa todas las preguntas.
    """
    resultado_final = {tipo: [] for tipo in tipos_disponibles}

    for tipo in tipos_disponibles:
        items = preguntas_contexto[tipo]
        if modo == "sample":
            items = items[:sample_size]  # solo algunas preguntas

        for item in items:
            pregunta = item.get("query", "").strip()
            if not pregunta:
                continue

            try:
                res = await consultar_votacion(pregunta)
            except Exception as e:
                res = {}

            docs = res.get("documents", [])
            if isinstance(docs, str):
                context_list = [docs]
            elif isinstance(docs, list):
                context_list = [d for d in docs if isinstance(d, str) and d.strip()]
            else:
                context_list = []

            resultado_final[tipo].append({"query": pregunta, "context": context_list})

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON guardado en: {OUTPUT_FILE}")


import asyncio

if __name__ == "__main__":
    asyncio.run(construir_contexto_qdrant(modo="all"))
    # await construir_contexto_qdrant(modo="sample", sample_size=2)
