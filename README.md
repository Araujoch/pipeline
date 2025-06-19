# Procesamiento de Texto 

Herramientas para limpieza, normalización y descarga de corpus de texto.  

## 🔥 Novedades (v2.1)
- **Todos los outputs ahora generan archivos en formato `.jsonl`** para mejor eficiencia en pipelines posteriores

## 📌 Resumen  
Este proyecto incluye herramientas mejoradas para el preprocesamiento de documentos de texto, con:  
- **Filtrado de contenido irrelevante** (`formatter`).  
- **Limpieza avanzada de "ruido"** (`encoder`).  
- **Descarga automatizada de datasets** (`downloaddatasets.py`).
- **Identificacion de Idioma**(`filter_lang`) 

---
## Los comandos deben ser ejecutados en el orden especificado en este documento

## 🛠️ Comandos  

### 1. `encoder`  
**Función**:  
    Corrige errores comunes en textos:

    Errores de codificación (ej.: UTF-8 mal interpretado).

    Etiquetas HTML/XML residuales.

Caracteres especiales no válidos.
**Uso**:  
    ./entrypoint.sh encoder --path  corpus/noisy/guarani.jsonl  --output  corpus/noisy/encoder_salida.jsonl

### 2. `formatter`  
**Función**:    
    Filtra documentos eliminando aquellos con menos de 2 palabras (para garantizar contenido relevante).  

**Uso**:  
    ./entrypoint.sh formatter --path corpus/noisy/encoder_salida.jsonl --delimiter \\n --output corpus/clean/formatter_salida.jsonl

### 3. `filter_lang`  
**Función**:    
    Identifica el lenguaje de cada uno de los documentos y descarga los que sean de baja confiabilidad
    - Añade función `advanced_text_filter` con heurísticas de calidad:  
    ✓ Capitalización consistente  
    ✓ Longitud de oraciones  
    ✓ Detección de repeticiones  
    ✓ Caracteres válidos  
    - Parametriza `reliability` (0.0-1.0) para filtrar por confianza en detección de idioma  

**Uso**:  
    ./entrypoint.sh filter_lang --path corpus/clean/formatter_salida.jsonl --output corpus/clean/filter_lang_salida.jsonl --filter_results_by_lang gn --reliability 0.8

### 4. `deduplication`
    Este comando permite deduplicar documentos basados en hashes, ideal para eliminar duplicados exactos o muy similares.

|**Parámetro**        |**Alias**| **Tipo** |**Requerido**|**Descripción                                                                                          |
| ------------------- | ------- | -------- | ---------   | --------------------------------------------------------------------------------------------------------- |
| `--path`            | `-p`    | `string` |      T      | Ruta absoluta al archivo de entrada `.jsonl`.                                                             |
| `--output`          | `-o`    | `string` |      F      | Ruta al archivo de salida con los documentos únicos.                                                      |
| `--input_lf`        | `-ilf`  | `int`    |      F      | Cantidad de saltos de línea (`\n`) que separan los documentos en el archivo de entrada. Por defecto: `3`. |
| `--output_lf`       | `-olf`  | `int`    |      F      | Cantidad de saltos de línea para separar los documentos en la salida. Por defecto: `2`.                   |
| `--threshold`       | `-t`    | `int`    |      F      | Documentos con menos palabras que este valor serán descartados. Por defecto: `15`.                        |
| `--save_duplicates` | `-s`    | `flag`   |      F      | Si se activa, guarda los duplicados detectados en un archivo separado.                                    |


**Uso**: 
    ./entrypoint.sh deduplication --path corpus/noisy/guarani.jsonl --output corpus/noisy/guarani_deduplication_output.jsonl -ilf 3 -olf 2 -t 15 -s

### 5. `jaccard(avanzado)`  
| **Parámetro**                      |**Alias**| **Tipo** |**Requerido**| Descripción                                                                        |
| ---------------------------------- |  ------ | -------- |      T      | ---------------------------------------------------------------------------------- |
| `--path`                           |  `-p`   | `string` |      F      | Ruta absoluta al archivo de entrada `.jsonl`.                                      |
| `--output_file`                    |  `-o`   | `flag`   |      F      | Si se incluye, guarda el archivo deduplicado en la misma carpeta que el original.  |
| `--max_documents`                  |  `-md`  | `int`    |      F      | Límite máximo de documentos a procesar (útil para pruebas).                        |
| `--length_threshold`               |  `-lt`  | `int`    |      F      | Longitud mínima del texto en tokens. Por defecto: `3`.                             |
| `--lsh_threshold`                  |  `-lsh` | `float`  |      F      | Umbral de similitud para LSH. Por defecto: `0.8`.                                  |
| `--generate_deduplication_samples` |  `-gds` | `flag`   |      F      | Si se activa, genera un archivo con ejemplos de duplicados para inspección manual. |

**Uso**:  
    ./entrypoint.sh jaccard --path corpus/noisy/guarani.jsonl -md 50 -lt 3 -lsh 0.75 -gds
