#!/bin/bash

# Ruta del directorio que contiene tus archivos .MOV
directorio_origen="/Users/efrainflores/Desktop/convert"

# Ruta del directorio donde quieres guardar los archivos convertidos
directorio_destino="/Users/efrainflores/Desktop/videos"

# Cambia al directorio de origen
cd "$directorio_origen"

# Bucle para procesar cada archivo .MOV
for archivo in *.MOV; do
    # Verifica si el archivo existe
    if [ -f "$archivo" ]; then
        # Nombre del archivo de salida (cambia la extensión a .mp4)
        nombre_archivo=$(basename "$archivo" .MOV)
        salida="$directorio_destino/$nombre_archivo.mp4"

        # Ejecuta ffmpeg para convertir el archivo
        ffmpeg -i "$archivo" -crf 0 "$salida"
    fi
done
