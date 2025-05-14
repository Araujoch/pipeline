# Procesamiento de Texto - Segunda Entrega  

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
**Uso**:  
    ./entrypoint.sh filter_lang --path corpus/clean/formatter_salida.jsonl --output corpus/clean/filter_lang_salida.jsonl --filter_results_by_lang gn


