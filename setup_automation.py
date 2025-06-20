#!/usr/bin/env python3
"""
Script de configuración rápida para automatización en la nube
"""

import os
import subprocess
import sys

def check_git():
    """Verifica si git está instalado y configurado"""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo():
    """Inicializa un repositorio git"""
    if not check_git():
        print("❌ Git no está instalado. Por favor instálalo primero.")
        return False
    
    try:
        # Inicializar git si no existe
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            print("✅ Repositorio git inicializado")
        
        # Añadir archivos
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Archivos añadidos al repositorio")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con git: {e}")
        return False

def create_github_repo():
    """Guía para crear repositorio en GitHub"""
    print("\n📋 Pasos para crear el repositorio en GitHub:")
    print("1. Ve a https://github.com/new")
    print("2. Crea un nuevo repositorio (por ejemplo: 'headlines-scraper')")
    print("3. NO inicialices con README (ya tenemos uno)")
    print("4. Copia la URL del repositorio")
    print("5. Ejecuta los siguientes comandos:")
    print("\n   git branch -M main")
    print("   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git")
    print("   git push -u origin main")

def setup_dropbox_token():
    """Guía para configurar token de Dropbox"""
    print("\n📋 Configuración de Dropbox:")
    print("1. Ve a https://www.dropbox.com/developers/apps")
    print("2. Crea una nueva app:")
    print("   - Choose an API: Scoped access")
    print("   - Choose the type of access: App folder")
    print("   - Name: headlines-scraper")
    print("3. En la app creada, ve a 'Permissions' y activa:")
    print("   - files.metadata.write")
    print("   - files.content.write")
    print("4. Ve a 'Settings' y genera un 'Generated access token'")
    print("5. Copia el token (empieza con 'sl.')")

def setup_github_secrets():
    """Guía para configurar secrets en GitHub"""
    print("\n📋 Configuración de GitHub Secrets:")
    print("1. Ve a tu repositorio en GitHub")
    print("2. Settings > Secrets and variables > Actions")
    print("3. 'New repository secret'")
    print("4. Añade:")
    print("   - Name: DROPBOX_ACCESS_TOKEN")
    print("   - Value: [tu token de Dropbox]")
    print("5. Guarda el secret")

def main():
    print("🚀 Configuración de Automatización en la Nube")
    print("=" * 50)
    
    # Verificar archivos necesarios
    required_files = ['headlines_scraper.py', '.github/workflows/daily_scraper_dropbox_api.yml']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Faltan archivos: {missing_files}")
        return
    
    print("✅ Archivos necesarios encontrados")
    
    # Inicializar git
    if init_git_repo():
        print("\n" + "=" * 50)
        create_github_repo()
        print("\n" + "=" * 50)
        setup_dropbox_token()
        print("\n" + "=" * 50)
        setup_github_secrets()
        
        print("\n🎉 ¡Configuración completada!")
        print("\n📱 Una vez configurado, podrás:")
        print("- Ver el HTML actualizado en la app de Dropbox")
        print("- Ejecutar manualmente desde GitHub Actions")
        print("- El script se ejecutará automáticamente cada día a las 10:00 AM")
    else:
        print("❌ Error en la configuración")

if __name__ == "__main__":
    main() 