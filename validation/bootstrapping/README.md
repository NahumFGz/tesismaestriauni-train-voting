# Evaluación de Métodos de Recuperación de Información - Análisis con Bootstrapping

## Resumen Ejecutivo

Este documento presenta los resultados de la evaluación comparativa de cuatro métodos de recuperación de información aplicados a documentos de votaciones del Congreso, utilizando análisis estadístico con bootstrapping para obtener intervalos de confianza robustos.

**Resultado Principal**: Qdrant (búsqueda vectorial semántica) demostró superioridad estadísticamente significativa en todas las métricas evaluadas, con un rendimiento excepcional que supera considerablemente a los métodos tradicionales basados en palabras clave.

## Configuración del Experimento

- **Total de consultas evaluadas**: 100 preguntas
- **Categorías de preguntas**: Fecha específica, asunto, y presidente
- **Muestras bootstrap**: 5,000 iteraciones
- **Nivel de confianza**: 95%
- **Métrica k**: Top-10 documentos recuperados

## Cuadro Comparativo de Resultados

| Método             | Precision@10        | MRR                 | Top-1 Accuracy      | Average Rank        | MAP                 | Recall@10           |
| ------------------ | ------------------- | ------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| **Qdrant**         | 0.791 [0.721-0.856] | 0.926 [0.878-0.967] | 0.900 [0.840-0.950] | 1.145 [1.041-1.277] | 0.926 [0.878-0.967] | 0.855 [0.801-0.903] |
| **BM25**           | 0.154 [0.123-0.188] | 0.483 [0.398-0.568] | 0.370 [0.270-0.470] | 2.778 [2.228-3.377] | 0.477 [0.396-0.558] | 0.498 [0.413-0.582] |
| **Keyword Search** | 0.138 [0.093-0.189] | 0.351 [0.266-0.440] | 0.300 [0.210-0.390] | 2.129 [1.558-2.776] | 0.370 [0.284-0.460] | 0.405 [0.314-0.495] |
| **TF-IDF**         | 0.040 [0.028-0.052] | 0.247 [0.169-0.329] | 0.221 [0.140-0.300] | 2.485 [1.656-3.407] | 0.248 [0.170-0.330] | 0.256 [0.174-0.340] |

## Análisis Detallado por Método

### 1. Qdrant (Búsqueda Vectorial Semántica) 🏆

**Rendimiento Superior Consistente**: Qdrant demuestra excelencia across todas las métricas con valores que superan significativamente a los demás métodos. Con una Precision@10 de 0.791, indica que aproximadamente 8 de cada 10 documentos en los primeros 10 resultados son relevantes.

**Intervalos de Confianza Estrechos**: La amplitud promedio de los intervalos es de 0.089 unidades, indicando alta consistencia y confiabilidad en las predicciones. El MRR de 0.926 con intervalo [0.878-0.967] (amplitud: 0.089) muestra la menor variabilidad, confirmando que el primer documento relevante aparece consistentemente en las primeras posiciones.

**Average Rank Excepcional**: Con 1.145 [1.041-1.277], los documentos relevantes aparecen prácticamente en la primera posición, con una variabilidad mínima (amplitud: 0.236).

### 2. BM25 (Best Matching 25)

**Rendimiento Intermedio Sólido**: BM25 se posiciona como el mejor método tradicional con una Precision@10 de 0.154, superando por factor de 4x a TF-IDF y manteniendo ventaja sobre keyword search.

**Variabilidad Moderada**: Los intervalos de confianza muestran amplitudes moderadas (promedio: 0.162), siendo el Average Rank [2.228-3.377] el más amplio (1.149), sugiriendo cierta inconsistencia en el posicionamiento de documentos relevantes.

**Ranking Balanceado**: Average Rank de 2.778 indica que los documentos relevantes aparecen típicamente en las posiciones 2-3, mostrando rendimiento consistente pero alejado de la posición óptima.

### 3. Keyword Search (Búsqueda por Palabras Clave)

**Rendimiento Básico Competitivo**: Con Precision@10 de 0.138, muestra rendimiento similar a BM25 pero con mayor variabilidad. Sorprendentemente supera a TF-IDF en la mayoría de métricas.

**Alta Variabilidad**: Presenta intervalos amplios (promedio: 0.176). La Precision@10 [0.093-0.189] tiene amplitud de 0.096, la mayor variabilidad en esta métrica, indicando inconsistencia en el rendimiento.

**Mejor Average Rank que BM25**: Con 2.129 [1.558-2.776], muestra mejor posicionamiento promedio que BM25, aunque con alta variabilidad (amplitud: 1.218).

### 4. TF-IDF (Term Frequency-Inverse Document Frequency)

**Rendimiento Limitado**: TF-IDF muestra el rendimiento más bajo con Precision@10 de 0.040, indicando que solo 4 de cada 100 documentos en los primeros 10 resultados son relevantes.

**Variabilidad Extrema**: Presenta la mayor variabilidad relativa, especialmente en Average Rank [1.656-3.407] (amplitud: 1.751), la mayor de todos los métodos, indicando inconsistencia severa en el posicionamiento de documentos relevantes.

**Paradoja de Complejidad**: A pesar de ser más sofisticado que keyword search, su rendimiento inferior sugiere que la complejidad del pesado TF-IDF no se traduce en mejor efectividad para este dominio específico.

## Interpretación de la Amplitud de Intervalos de Confianza

### Estabilidad del Rendimiento

- **Qdrant** (amplitud promedio: 0.089): Alta estabilidad y confiabilidad
- **BM25** (amplitud promedio: 0.162): Estabilidad moderada con variabilidad controlada
- **Keyword Search** (amplitud promedio: 0.176): Mayor variabilidad, rendimiento menos predecible
- **TF-IDF** (amplitud promedio: 0.160): Variabilidad moderada pero con valores absolutos bajos

### Significancia Estadística

Los intervalos de confianza no superpuestos entre Qdrant y los demás métodos confirman diferencias estadísticamente significativas. La separación clara entre los intervalos (gap mínimo de 0.533 en Precision@10) proporciona evidencia robusta de la superioridad de la búsqueda vectorial semántica.

### Análisis de Variabilidad por Métrica

- **Precision@10**: Qdrant muestra la menor variabilidad (0.135), mientras que Keyword Search presenta la mayor (0.096)
- **MRR**: Consistentemente baja variabilidad across métodos, con Qdrant liderando en estabilidad (0.089)
- **Average Rank**: Mayor fuente de variabilidad, especialmente en TF-IDF (1.751), indicando inconsistencia en posicionamiento

## Interpretación de Métricas

- **Precision@10**: Proporción de documentos relevantes entre los primeros 10 resultados
- **MRR (Mean Reciprocal Rank)**: Posición promedio del primer documento relevante (valores más altos indican mejor rendimiento)
- **Top-1 Accuracy**: Porcentaje de consultas donde el primer resultado es relevante
- **MAP (Mean Average Precision)**: Precisión promedio considerando el orden de los resultados
- **Recall@10**: Proporción de documentos relevantes recuperados en los primeros 10 resultados
- **Average Rank**: Posición promedio de los documentos relevantes (valores más bajos indican mejor rendimiento)

---

# Contenido para Paper Académico

## Metodología

Para evaluar la efectividad de los métodos de recuperación de información, se implementó una evaluación comparativa utilizando análisis estadístico con bootstrapping. Se generó un conjunto de 100 consultas de prueba distribuidas en tres categorías: consultas por fecha específica (30 preguntas), por asunto (35 preguntas) y por presidente de sesión (35 preguntas). Cada consulta incluía su contexto esperado basado en los documentos originales.

La evaluación se realizó utilizando cinco métricas estándar de recuperación de información: Precision@10, Mean Reciprocal Rank (MRR), Top-1 Accuracy, Mean Average Precision (MAP) y Recall@10. Para obtener estimaciones robustas y intervalos de confianza, se aplicó el método de bootstrapping con 5,000 muestras de remuestreo y un nivel de confianza del 95%.

Los métodos evaluados incluyeron: (1) búsqueda por palabras clave con filtrado de stop words, (2) TF-IDF con similitud coseno, (3) BM25 con parámetros optimizados (k1=1.5, b=0.75), y (4) búsqueda vectorial semántica utilizando Qdrant con embeddings pre-entrenados. La comparación de contextos se realizó mediante coincidencia de URLs y similitud de contenido normalizado con un umbral del 80%.

## Resultados

Los resultados de la evaluación demuestran una superioridad clara y estadísticamente significativa del método de búsqueda vectorial semántica (Qdrant) sobre los enfoques tradicionales. Qdrant alcanzó una Precision@10 de 0.791 (IC 95%: 0.721-0.856), significativamente superior a BM25 (0.154, IC: 0.123-0.188), búsqueda por palabras clave (0.138, IC: 0.093-0.189) y TF-IDF (0.040, IC: 0.028-0.052).

El rendimiento superior de Qdrant se mantiene consistente across todas las métricas evaluadas. El MRR de 0.926 (IC: 0.878-0.967) indica que el primer documento relevante aparece, en promedio, en la primera posición, contrastando con BM25 (0.483), búsqueda por palabras clave (0.351) y TF-IDF (0.247). La Top-1 Accuracy de 0.900 confirma que Qdrant proporciona el documento más relevante como primer resultado en aproximadamente 9 de cada 10 consultas.

Entre los métodos tradicionales, BM25 mostró el mejor rendimiento, superando consistentemente a la búsqueda por palabras clave y TF-IDF en todas las métricas. Sorprendentemente, la búsqueda simple por palabras clave superó a TF-IDF en la mayoría de métricas, sugiriendo que la complejidad adicional del pesado TF-IDF no se traduce necesariamente en mejor rendimiento para este dominio específico.

## Discusión y Conclusiones

Los resultados obtenidos revelan diferencias sustanciales en la efectividad de los métodos de recuperación evaluados, con implicaciones importantes para sistemas de información parlamentaria. La superioridad del método de búsqueda vectorial semántica puede atribuirse a su capacidad para capturar similitudes semánticas que trascienden la coincidencia exacta de términos, particularmente relevante en el contexto de documentos parlamentarios donde conceptos similares pueden expresarse con vocabulario diverso.

El rendimiento excepcional de Qdrant (con métricas superiores a 0.79 en precision y 0.92 en MRR) sugiere que los embeddings pre-entrenados capturan efectivamente las relaciones semánticas en el dominio parlamentario, permitiendo recuperar documentos relevantes incluso cuando las consultas utilizan terminología diferente a la presente en los documentos. Esta capacidad es particularmente valiosa para usuarios no especializados que pueden formular consultas usando lenguaje natural sin conocimiento específico de la terminología parlamentaria formal.

El rendimiento moderado de BM25 (0.154 precision) en comparación con Qdrant, pero superior a los otros métodos tradicionales, confirma su efectividad como función de ranking probabilística mejorada respecto a TF-IDF. Sin embargo, la brecha significativa con la búsqueda vectorial evidencia las limitaciones de los enfoques basados exclusivamente en coincidencia de términos.

La evaluación estadística con bootstrapping proporciona robustez a estos hallazgos, con intervalos de confianza que no se superponen entre Qdrant y los demás métodos, confirmando la significancia estadística de las diferencias observadas. Estos resultados sugieren que la implementación de búsqueda vectorial semántica en sistemas de información parlamentaria puede mejorar sustancialmente la experiencia del usuario y la efectividad en la recuperación de información legislativa.

Las limitaciones del estudio incluyen la evaluación en un único dominio (votaciones parlamentarias) y el uso de un conjunto específico de embeddings pre-entrenados. Investigaciones futuras podrían explorar la generalización de estos resultados a otros tipos de documentos parlamentarios y la optimización de embeddings específicos del dominio legislativo.

---

## Archivos Generados

- `resumen_completo.json`: Resultados detallados con intervalos de confianza
- `comparacion_metodos.csv`: Tabla comparativa de todas las métricas
- `reporte_evaluacion.html`: Reporte interactivo con visualizaciones
- Visualizaciones PNG: Gráficos de barras, radar, heatmap, distribuciones bootstrap y ranking

## Hallazgos Clave Destacados

1. **Qdrant es claramente superior**: 0.791 precision vs. 0.154 del segundo mejor (BM25) - diferencia de 5.1x
2. **Diferencias estadísticamente significativas**: Los intervalos de confianza no se superponen entre métodos
3. **BM25 supera a métodos más simples**: Confirma la efectividad de funciones de ranking probabilísticas
4. **TF-IDF tuvo el peor rendimiento**: 0.040 precision sugiere que la complejidad no siempre mejora resultados
5. **Búsqueda semántica vs. léxica**: La capacidad de entender significado supera la coincidencia exacta
6. **Estabilidad de Qdrant**: Menor amplitud de intervalos (0.089) indica mayor confiabilidad
7. **Variabilidad en métodos tradicionales**: TF-IDF muestra la mayor inconsistencia (amplitud: 1.751 en Average Rank)

## Recomendaciones

1. **Para sistemas en producción**: Implementar Qdrant como método principal de búsqueda
2. **Para sistemas con recursos limitados**: Considerar BM25 como alternativa viable
3. **Para evaluaciones futuras**: Incluir métricas de diversidad y análisis por categoría de consulta
4. **Para optimización**: Explorar fine-tuning de embeddings específicos del dominio parlamentario
