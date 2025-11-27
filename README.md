# tesismaestriauni-train-voting

## Descripción

Este proyecto es parte de la tesis de maestría "Desarrollo de un modelo conversacional para la transparencia gubernamental del Estado peruano". Específicamente, este repositorio contiene el entrenamiento y pruebas del sistema RAG (Retrieval Augmented Generation) para el módulo de conducta parlamentaria, enfocado en el análisis de asistencias y votaciones de congresistas peruanos.

## Contexto del Proyecto

Este proyecto forma parte de un sistema más grande que incluye:

- Módulo de contrataciones públicas (SUNAT, OSCE, MEF)
- Módulo de conducta parlamentaria (asistencias y votaciones 2006-2024)
- Modelo conversacional basado en LangGraph y LangChain
- Implementación distribuida con microservicios MCP (Model Context Protocol)

## Estructura del Proyecto

### Directorios Principales

- `notebooks/`: Contiene los notebooks de Jupyter para el entrenamiento del RAG

  - `a_generar_documentos.ipynb`: Notebook para la generación y procesamiento de documentos de votación
  - `b_cargar_documents.ipynb`: Notebook para la carga y enriquecimiento de documentos en el sistema RAG

- `notebooks_rag/`: Directorio para experimentos y pruebas del sistema RAG

  - Contiene notebooks para pruebas de recuperación y generación de respuestas
  - Experimentos con diferentes estrategias de chunking y embedding

- `data/`: Almacena los datos procesados

  - `attendance_docs_votacion_enriched.json`: Documentos de votación enriquecidos con metadatos

- `tools/`: Directorio para pruebas del MCP (Model Context Protocol)

  - Implementaciones de prueba del protocolo de contexto
  - Herramientas para validación y monitoreo
  - Scripts de utilidad para el procesamiento de documentos

- `validation/`: Herramientas y scripts para validación
  - Métricas de evaluación (hit@k, precision, recall)
  - Tests de calidad de respuestas
  - Validación de recuperación de documentos

### Archivos de Configuración

- `pyproject.toml`: Configuración del proyecto y dependencias
- `poetry.lock`: Bloqueo de versiones de dependencias
- `.gitignore`: Configuración de archivos ignorados

## Tecnologías Utilizadas

### Procesamiento de Documentos

- OCR: Doctr, PaddleOCR
- Procesamiento de Imágenes: OpenCV, Pillow

### Procesamiento de Lenguaje Natural

- LangChain y LangGraph para el sistema RAG
- Qdrant para almacenamiento vectorial
- OpenAI text-embedding-3-small para embeddings

### Análisis de Datos

- Pandas para manipulación de datos
- SQLAlchemy para interacción con bases de datos

### Desarrollo

- Jupyter para notebooks interactivos
- Python 3.10 como lenguaje base

## Flujo de Trabajo

1. **Preparación de Datos**

   - Generación de documentos (`a_generar_documentos.ipynb`)
   - Procesamiento OCR de documentos escaneados
   - Enriquecimiento con metadatos

2. **Sistema RAG**

   - Carga de documentos (`b_cargar_documents.ipynb`)
   - Segmentación con RecursiveCharacterTextSplitter
   - Generación de embeddings
   - Almacenamiento en Qdrant

3. **Validación y Pruebas**
   - Evaluación de recuperación de documentos
   - Pruebas de generación de respuestas
   - Métricas de rendimiento

## Requisitos del Sistema

- Python >=3.11, <3.12
- Poetry para gestión de dependencias
- Acceso a OpenAI API para embeddings

## Instalación

1. Clonar el repositorio
2. Instalar Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
3. Instalar dependencias: `poetry install`
4. Activar entorno: `poetry shell`

## Uso

1. Ejecutar el flujo de procesamiento:

   ```bash
   # 1. Generar documentos
   jupyter notebook notebooks/a_generar_documentos.ipynb

   # 2. Cargar y procesar documentos
   jupyter notebook notebooks/b_cargar_documents.ipynb
   ```
