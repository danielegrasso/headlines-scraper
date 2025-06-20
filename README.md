# 📰 Scraper de Titulares Automatizado

Script para extraer titulares de El Mundo, El Confidencial y El Diario, con secciones especiales de "Datos y Gráficos".

## 🚀 Configuración para Automatización en la Nube

### Opción 1: GitHub Actions (Recomendada - GRATIS)

#### Pasos de configuración:

1. **Subir el código a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```

2. **Configurar Dropbox como servidor FTP:**
   - Ve a [Dropbox.com](https://www.dropbox.com)
   - En tu cuenta, ve a Configuración > Cuenta
   - Activa "FTP y WebDAV"
   - Anota los datos de conexión FTP

3. **Configurar secrets en GitHub:**
   - Ve a tu repositorio en GitHub
   - Settings > Secrets and variables > Actions
   - Añade estos secrets:
     - `FTP_SERVER`: Tu servidor FTP de Dropbox
     - `FTP_USERNAME`: Tu usuario FTP
     - `FTP_PASSWORD`: Tu contraseña FTP

4. **¡Listo!** El script se ejecutará automáticamente todos los días a las 10:00 AM (hora española).

### Opción 2: Heroku (Alternativa)

Si prefieres Heroku, puedes usar:

```bash
# Crear app en Heroku
heroku create tu-app-name

# Configurar scheduler
heroku addons:create scheduler:standard

# Subir código
git push heroku main

# Programar tarea diaria
heroku scheduler:add "python headlines_scraper.py" --dyno=basic --frequency=daily
```

### Opción 3: PythonAnywhere (Alternativa)

1. Crea cuenta en [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Sube el script
3. Configura una tarea programada en la sección "Tasks"

## 📱 Acceso desde el móvil

Una vez configurado, podrás:

1. **Ver el HTML actualizado** abriendo la app de Dropbox en tu móvil
2. **Ejecutar manualmente** desde GitHub Actions (Actions > Run workflow)
3. **Recibir notificaciones** configurando webhooks

## 🔧 Configuración local

Para ejecutar manualmente:

```bash
python3 headlines_scraper.py
```

## 📊 Características

- ✅ Extrae 4 titulares principales de cada periódico
- ✅ Sección "Datos y Gráficos" con autores especializados
- ✅ Indicador de artículos nuevos del día
- ✅ Limpieza automática de archivos antiguos
- ✅ HTML responsive y bien formateado
- ✅ Ejecución automática diaria

## 🛠️ Dependencias

```
requests
beautifulsoup4
```

## 📝 Notas

- El script detecta automáticamente artículos nuevos basándose en la fecha en la URL
- Los archivos antiguos (más de 2 días) se eliminan automáticamente
- El HTML se genera con timestamp para evitar conflictos 