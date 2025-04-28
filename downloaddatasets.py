from datasets import load_dataset
import os

try:
    # Cargar el dataset
    dataset = load_dataset("HuggingFaceFW/fineweb-2", "gug_Latn", split="train")
    
    # Ruta absoluta para el archivo de salida
    output_path = os.path.abspath("guarani.jsonl")
    
    # Guardar en JSONL
    dataset.to_json(output_path, orient="records", lines=True)
    
    print(f"Archivo guardado en: {output_path}")
    print(f"Tamaño del dataset: {len(dataset)} registros")

except Exception as e:
    print(f"Error: {e}")
    print("Verifica:")
    print("- El nombre del dataset y la configuración (gug_Latn)")
    print("- Que la partición 'train' exista")
    print("- Permisos de escritura en el directorio")