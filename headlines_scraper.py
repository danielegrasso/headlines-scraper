#!/usr/bin/env python3
"""
Script para extraer los primeros cuatro titulares de tres periódicos
y guardarlos en un archivo HTML.
"""

import requests
from bs4 import BeautifulSoup
import html
from datetime import datetime
import os
import re

def is_article_from_today(link, title):
    """Determina si un artículo es del día actual basándose en la URL y título"""
    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d')
    today_str_short = today.strftime('%Y%m%d')
    
    # Buscar patrones de fecha en la URL
    date_patterns = [
        today_str,  # 2025-06-20
        today_str_short,  # 20250620
        today.strftime('%Y/%m/%d'),  # 2025/06/20
        today.strftime('%Y/%m'),  # 2025/06
    ]
    
    for pattern in date_patterns:
        if pattern in link:
            return True
    
    # Buscar en el título palabras que indiquen "hoy" o "actual"
    today_indicators = ['hoy', 'actual', 'última hora', 'breaking', 'ahora']
    for indicator in today_indicators:
        if indicator.lower() in title.lower():
            return True
    
    return False

def get_headlines_el_mundo():
    """Extrae los primeros 4 titulares de El Mundo"""
    try:
        url = "https://www.elmundo.es"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = []
        
        # Buscar titulares en selectores más específicos de El Mundo
        selectors = [
            '.ue-c-cover-content__headline a',  # Titulares principales
            '.ue-c-cover-content__title a',     # Títulos principales
            '.ue-c-cover-content__link',        # Enlaces principales
            'h1 a', 'h2 a', 'h3 a',             # Encabezados
            '.headline a', '.title a'           # Selectores genéricos
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                if element.get_text().strip() and len(headlines) < 4:
                    title = element.get_text().strip()
                    link = element.get('href', '')
                    
                    # Filtrar elementos que no son titulares de noticias
                    if (len(title) > 10 and  # Títulos muy cortos probablemente no son noticias
                        not title.isupper() and  # Evitar títulos en mayúsculas (como "MUNDIAL DE CLUBES")
                        not title.startswith('CARLOS') and  # Evitar nombres de autores
                        not 'comentarios' in title.lower() and  # Evitar contadores de comentarios
                        not title.startswith('MUNDIAL') and  # Evitar secciones deportivas
                        link and  # Debe tener enlace
                        not link.endswith('.html#ancla_comentarios')):  # Evitar enlaces a comentarios
                        
                        if not link.startswith('http'):
                            link = 'https://www.elmundo.es' + link
                        headlines.append({'title': title, 'link': link, 'source': 'El Mundo'})
                        if len(headlines) >= 4:
                            break
            if len(headlines) >= 4:
                break
                
        return headlines[:4]
    except Exception as e:
        print(f"Error extrayendo de El Mundo: {e}")
        return []

def get_latest_article_author(url, author_name):
    """Extrae el último artículo de un autor específico (El Mundo)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Buscar el primer bloque de artículo real
        block = soup.select_one('.ue-c-cover-content')
        if block:
            link_tag = block.find('a', href=True)
            if link_tag and link_tag.get_text().strip():
                title = link_tag.get_text().strip()
                link = link_tag['href']
                if not link.startswith('http'):
                    link = 'https://www.elmundo.es' + link
                
                is_new = is_article_from_today(link, title)
                return {'title': title, 'link': link, 'author': author_name, 'is_new': is_new}
        return None
    except Exception as e:
        print(f"Error extrayendo artículo de {author_name}: {e}")
        return None

def get_data_articles_el_mundo():
    """Extrae los últimos artículos de los autores de datos de El Mundo"""
    authors = [
        ('https://www.elmundo.es/autor/maria-alcantara.html', 'María Alcántara'),
        ('https://www.elmundo.es/autor/emilio-amade.html', 'Emilio Amade'),
        ('https://www.elmundo.es/autor/javier-aguirre.html', 'Javier Aguirre'),
        ('https://www.elmundo.es/autor/alberto-hernandez.html', 'Alberto Hernández')
    ]
    
    articles = []
    for url, author_name in authors:
        article = get_latest_article_author(url, author_name)
        if article:
            articles.append(article)
    
    return articles

def get_latest_article_author_confidencial(url, author_name):
    """Extrae el último artículo de un autor específico de El Confidencial"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Buscar el primer artículo en la clase archive-article-top-tit
        article_link = soup.select_one('.archive-article-top-tit a')
        if article_link and article_link.get_text().strip():
            title = article_link.get_text().strip()
            link = article_link['href']
            if not link.startswith('http'):
                link = 'https://www.elconfidencial.com' + link
            
            is_new = is_article_from_today(link, title)
            return {'title': title, 'link': link, 'author': author_name, 'is_new': is_new}
        return None
    except Exception as e:
        print(f"Error extrayendo artículo de {author_name}: {e}")
        return None

def get_data_articles_el_confidencial():
    """Extrae los últimos artículos de los autores de datos de El Confidencial"""
    authors = [
        ('https://www.elconfidencial.com/autores/miguel-angel-gavilanes-5390/', 'Miguel Ángel Gavilanes'),
        ('https://www.elconfidencial.com/autores/marta-ley-4163/', 'Marta Ley')
    ]
    
    articles = []
    for url, author_name in authors:
        article = get_latest_article_author_confidencial(url, author_name)
        if article:
            articles.append(article)
    
    return articles

def get_latest_article_author_eldiario(url, author_name):
    """Extrae el último artículo de un autor específico de El Diario"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Buscar el primer artículo real en la página del autor
        # Intentar diferentes selectores para encontrar el artículo más reciente
        selectors = [
            '.article-author-cont h2 a',  # Títulos de artículos en contenedor de autor
            '.article-author-cont h3 a',  # Subtítulos de artículos
            '.article-author-cont .title a',  # Títulos con clase específica
            '.article-author-cont a[href*="/"]',  # Enlaces que contienen "/" (artículos)
            '.article-author-cont a'  # Cualquier enlace en el contenedor
        ]
        
        for selector in selectors:
            article_links = soup.select(selector)
            for link in article_links:
                title = link.get_text().strip()
                href = link.get('href', '')
                # Filtrar enlaces que parecen ser artículos reales
                if (title and 
                    len(title) > 10 and  # Títulos largos
                    href and 
                    '/' in href and  # Contiene "/" (indicador de artículo)
                    not title.lower() in ['euskadi', 'economía', 'política', 'sociedad', 'internacional'] and  # Evitar enlaces de navegación
                    not href.startswith('#')):  # Evitar enlaces internos
                    
                    if not href.startswith('http'):
                        href = 'https://www.eldiario.es' + href
                    
                    is_new = is_article_from_today(href, title)
                    return {'title': title, 'link': href, 'author': author_name, 'is_new': is_new}
        return None
    except Exception as e:
        print(f"Error extrayendo artículo de {author_name}: {e}")
        return None

def get_data_articles_el_diario():
    """Extrae los últimos artículos de los autores de datos de El Diario"""
    authors = [
        ('https://www.eldiario.es/autores/raul_sanchez/', 'Raúl Sánchez'),
        ('https://www.eldiario.es/autores/victoria_oliveres/', 'Victoria Oliveres')
    ]
    
    articles = []
    for url, author_name in authors:
        article = get_latest_article_author_eldiario(url, author_name)
        if article:
            articles.append(article)
    
    return articles

def get_headlines_el_confidencial():
    """Extrae los primeros 4 titulares de El Confidencial"""
    try:
        url = "https://www.elconfidencial.com"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = []
        
        # Buscar titulares en selectores específicos de El Confidencial
        selectors = [
            '.gac-principal__titleLink',  # Primer titular principal
            '.m-principal a',             # Segundo titular principal
            '.m-fotoCentral__titleSide a', # Tercer titular principal
            '.c-85__titleSide a',         # Cuarto titular principal (la 85)
            '.article-title a', '.headline-title a',
            'h2 a', 'h3 a', '.headline a', '.title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                if element.get_text().strip() and len(headlines) < 4:
                    title = element.get_text().strip()
                    link = element.get('href', '')
                    if not link.startswith('http'):
                        link = 'https://www.elconfidencial.com' + link
                    headlines.append({'title': title, 'link': link, 'source': 'El Confidencial'})
                    if len(headlines) >= 4:
                        break
            if len(headlines) >= 4:
                break
                
        return headlines[:4]
    except Exception as e:
        print(f"Error extrayendo de El Confidencial: {e}")
        return []

def get_headlines_el_diario():
    """Extrae los primeros 4 titulares de El Diario"""
    try:
        url = "https://www.eldiario.es"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = []
        
        selectors = [
            'h2 a', 'h3 a', '.headline a', '.title a', 
            '.article-title a', '.headline-title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                if element.get_text().strip() and len(headlines) < 4:
                    title = element.get_text().strip()
                    link = element.get('href', '')
                    if not link.startswith('http'):
                        link = 'https://www.eldiario.es' + link
                    headlines.append({'title': title, 'link': link, 'source': 'El Diario'})
                    if len(headlines) >= 4:
                        break
            if len(headlines) >= 4:
                break
                
        return headlines[:4]
    except Exception as e:
        print(f"Error extrayendo de El Diario: {e}")
        return []

def clean_old_files():
    """Elimina archivos HTML de titulares de días anteriores"""
    try:
        current_time = datetime.now()
        files_to_delete = []
        
        # Buscar archivos de titulares en el directorio actual
        for filename in os.listdir('.'):
            if filename.startswith('titulares_') and filename.endswith('.html'):
                # Extraer la fecha del nombre del archivo
                try:
                    # Formato: titulares_YYYYMMDD_HHMMSS.html
                    date_str = filename.split('_')[1] + '_' + filename.split('_')[2].split('.')[0]
                    file_time = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                    
                    # Eliminar archivos de hace más de 2 días
                    if (current_time - file_time).days > 2:
                        files_to_delete.append(filename)
                except:
                    continue
        
        # Eliminar archivos antiguos
        for filename in files_to_delete:
            try:
                os.remove(filename)
                print(f"🗑️ Eliminado archivo antiguo: {filename}")
            except Exception as e:
                print(f"Error eliminando {filename}: {e}")
                
    except Exception as e:
        print(f"Error limpiando archivos antiguos: {e}")

def create_html_file(all_headlines, data_articles_el_mundo, data_articles_el_confidencial, data_articles_el_diario):
    """Crea un archivo HTML con todos los titulares y artículos de datos"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titulares de Periódicos - {timestamp}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .newspaper-section {{
            margin-bottom: 30px;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .newspaper-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
            color: #333;
        }}
        .data-section {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #667eea;
        }}
        .data-title {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .status-indicator {{
            font-size: 14px;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: normal;
        }}
        .status-new {{
            background-color: #28a745;
            color: white;
        }}
        .status-old {{
            background-color: #6c757d;
            color: white;
        }}
        .headline {{
            margin-bottom: 15px;
            padding: 10px;
            border-left: 4px solid #667eea;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
        }}
        .headline:hover {{
            background-color: #e9ecef;
            transform: translateX(5px);
        }}
        .headline a {{
            color: #333;
            text-decoration: none;
            font-size: 16px;
            line-height: 1.4;
        }}
        .headline a:hover {{
            color: #667eea;
        }}
        .author-name {{
            font-size: 14px;
            color: #666;
            font-style: italic;
            margin-top: 5px;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 20px;
        }}
        .error {{
            color: #dc3545;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📰 Titulares de Periódicos</h1>
        <p>Actualizado el {timestamp}</p>
    </div>
"""
    
    newspapers = {}
    for headline in all_headlines:
        source = headline['source']
        if source not in newspapers:
            newspapers[source] = []
        newspapers[source].append(headline)
    
    for newspaper, headlines in newspapers.items():
        html_content += f"""
    <div class="newspaper-section">
        <div class="newspaper-title">📰 {newspaper}</div>
"""
        
        if headlines:
            for i, headline in enumerate(headlines, 1):
                html_content += f"""
        <div class="headline">
            <a href="{html.escape(headline['link'])}" target="_blank">{i}. {html.escape(headline['title'])}</a>
        </div>
"""
        else:
            html_content += f"""
        <div class="headline error">
            No se pudieron extraer titulares de {newspaper}
        </div>
"""
        
        # Añadir sección de datos para El Mundo
        if newspaper == 'El Mundo' and data_articles_el_mundo:
            # Contar artículos nuevos
            new_articles_count = sum(1 for article in data_articles_el_mundo if article.get('is_new', False))
            status_text = "Hay artículos nuevos" if new_articles_count > 0 else "Sin novedades"
            status_class = "status-new" if new_articles_count > 0 else "status-old"
            
            html_content += f"""
        <div class="data-section">
            <div class="data-title">
                <span>📊 Datos y Gráficos</span>
                <span class="status-indicator {status_class}">{status_text}</span>
            </div>
"""
            for article in data_articles_el_mundo:
                html_content += f"""
            <div class="headline">
                <a href="{html.escape(article['link'])}" target="_blank">{html.escape(article['title'])}</a>
                <div class="author-name">Por {article['author']}</div>
            </div>
"""
            html_content += """
        </div>
"""
        
        # Añadir sección de datos para El Confidencial
        if newspaper == 'El Confidencial' and data_articles_el_confidencial:
            # Contar artículos nuevos
            new_articles_count = sum(1 for article in data_articles_el_confidencial if article.get('is_new', False))
            status_text = "Hay artículos nuevos" if new_articles_count > 0 else "Sin novedades"
            status_class = "status-new" if new_articles_count > 0 else "status-old"
            
            html_content += f"""
        <div class="data-section">
            <div class="data-title">
                <span>📊 Datos y Gráficos</span>
                <span class="status-indicator {status_class}">{status_text}</span>
            </div>
"""
            for article in data_articles_el_confidencial:
                html_content += f"""
            <div class="headline">
                <a href="{html.escape(article['link'])}" target="_blank">{html.escape(article['title'])}</a>
                <div class="author-name">Por {article['author']}</div>
            </div>
"""
            html_content += """
        </div>
"""
        
        # Añadir sección de datos para El Diario
        if newspaper == 'El Diario' and data_articles_el_diario:
            # Contar artículos nuevos
            new_articles_count = sum(1 for article in data_articles_el_diario if article.get('is_new', False))
            status_text = "Hay artículos nuevos" if new_articles_count > 0 else "Sin novedades"
            status_class = "status-new" if new_articles_count > 0 else "status-old"
            
            html_content += f"""
        <div class="data-section">
            <div class="data-title">
                <span>📊 Datos y Gráficos</span>
                <span class="status-indicator {status_class}">{status_text}</span>
            </div>
"""
            for article in data_articles_el_diario:
                html_content += f"""
            <div class="headline">
                <a href="{html.escape(article['link'])}" target="_blank">{html.escape(article['title'])}</a>
                <div class="author-name">Por {article['author']}</div>
            </div>
"""
            html_content += """
        </div>
"""
        
        html_content += """
    </div>
"""
    
    html_content += f"""
    <div class="timestamp">
        Script ejecutado el {timestamp}
    </div>
</body>
</html>"""
    
    filename = f"titulares_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def main():
    """Función principal que ejecuta todo el proceso"""
    print("🚀 Iniciando extracción de titulares...")
    
    # Limpiar archivos antiguos
    print("🧹 Limpiando archivos antiguos...")
    clean_old_files()
    
    all_headlines = []
    
    print("📰 Extrayendo de El Mundo...")
    all_headlines.extend(get_headlines_el_mundo())
    
    print("📰 Extrayendo de El Confidencial...")
    all_headlines.extend(get_headlines_el_confidencial())
    
    print("📰 Extrayendo de El Diario...")
    all_headlines.extend(get_headlines_el_diario())
    
    print("📊 Extrayendo artículos de datos de El Mundo...")
    data_articles_el_mundo = get_data_articles_el_mundo()
    
    print("📊 Extrayendo artículos de datos de El Confidencial...")
    data_articles_el_confidencial = get_data_articles_el_confidencial()
    
    print("📊 Extrayendo artículos de datos de El Diario...")
    data_articles_el_diario = get_data_articles_el_diario()
    
    print("💾 Creando archivo HTML...")
    filename = create_html_file(all_headlines, data_articles_el_mundo, data_articles_el_confidencial, data_articles_el_diario)
    
    print(f"✅ ¡Completado! Se han extraído {len(all_headlines)} titulares")
    print(f"📊 Se han extraído {len(data_articles_el_mundo)} artículos de datos de El Mundo")
    print(f"📊 Se han extraído {len(data_articles_el_confidencial)} artículos de datos de El Confidencial")
    print(f"📊 Se han extraído {len(data_articles_el_diario)} artículos de datos de El Diario")
    print(f"📄 Archivo guardado como: {filename}")
    print(f"🌐 Abre {filename} en tu navegador para ver los resultados")

if __name__ == "__main__":
    main() 