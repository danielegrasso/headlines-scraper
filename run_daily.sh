#!/bin/bash

# Script para ejecutar el extractor de titulares diariamente
# Cambiar al directorio del script
cd "$(dirname "$0")"

# Ejecutar el script de Python
python3 headlines_scraper.py

# Opcional: Abrir el archivo HTML generado en el navegador
# (descomenta la línea siguiente si quieres que se abra automáticamente)
# open titulares_*.html 