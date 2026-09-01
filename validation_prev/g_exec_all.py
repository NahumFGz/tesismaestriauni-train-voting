#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecuta secuencialmente el pipeline completo de validation_prev:
a_base_pruebas -> b_recuperacion_qdrant -> c_keyword_search_baseline
-> d_tf_idf_baseline -> e_bm25_baseline -> f_boostraping.
"""

import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

PIPELINE = [
    "a_base_pruebas.py",
    "b_recuperacion_qdrant.py",
    "c_keyword_search_baseline.py",
    "d_tf_idf_baseline.py",
    "e_bm25_baseline.py",
    "f_boostraping.py",
]


def main() -> None:
    inicio_total = time.perf_counter()

    for i, script in enumerate(PIPELINE, start=1):
        script_path = SCRIPT_DIR / script
        print(f"\n{'=' * 70}")
        print(f"▶️  [{i}/{len(PIPELINE)}] Ejecutando {script}")
        print(f"{'=' * 70}\n")

        inicio = time.perf_counter()
        resultado = subprocess.run([sys.executable, str(script_path)], cwd=SCRIPT_DIR)
        duracion = time.perf_counter() - inicio

        if resultado.returncode != 0:
            print(f"\n❌ {script} falló (código {resultado.returncode}) tras {duracion:.1f}s")
            print("⏹️  Deteniendo el pipeline.")
            sys.exit(resultado.returncode)

        print(f"\n✅ {script} completado en {duracion:.1f}s")

    duracion_total = time.perf_counter() - inicio_total
    print(f"\n{'=' * 70}")
    print(f"🏁 Pipeline completo en {duracion_total:.1f}s")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
