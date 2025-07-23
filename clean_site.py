#!/usr/bin/env python3
"""
Script para limpiar el sitio web estático
Elimina dependencias externas y optimiza el código
"""

import re
import os

def clean_html_file(file_path):
    """Limpia un archivo HTML de referencias externas"""
    print(f"Limpiando {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar URLs absolutas por relativas
    content = re.sub(r'https://maestrogregorio\.com/', '', content)
    
    # Eliminar Google Analytics y tracking scripts
    content = re.sub(r'<!-- Google Tag Manager.*?<!-- End Google Tag Manager.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*gtag[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*google-analytics[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    
    # Eliminar referencias a Google Fonts
    content = re.sub(r"<link[^>]*fonts\.googleapis\.com[^>]*>", '', content)
    content = re.sub(r"<link[^>]*fonts\.gstatic\.com[^>]*>", '', content)
    
    # Eliminar pingback y referencias externas
    content = re.sub(r'<link rel=["\']pingback["\'][^>]*>', '', content)
    content = re.sub(r'<link rel=["\']dns-prefetch["\'][^>]*>', '', content)
    
    # Eliminar referencias a feeds RSS (ya eliminamos los directorios)
    content = re.sub(r'<link[^>]*application/rss\+xml[^>]*>', '', content)
    
    # Eliminar referencias a API de WordPress
    content = re.sub(r'<link rel=["\']https://api\.w\.org/["\'][^>]*>', '', content)
    content = re.sub(r'<link rel=["\']EditURI["\'][^>]*>', '', content)
    
    # Limpiar configuraciones de JavaScript que contienen URLs externas
    content = re.sub(r'"ajaxurl":"https://maestrogregorio\.com/wp-admin/admin-ajax\.php"', '"ajaxurl":"wp-admin/admin-ajax.php"', content)
    content = re.sub(r'"page_permalink":"https://maestrogregorio\.com/"', '"page_permalink":"./"', content)
    
    # Eliminar scripts de chat externos (Chaty)
    content = re.sub(r'<script[^>]*chaty[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'var chaty_settings = \{.*?\};', '', content, flags=re.DOTALL)
    
    # Eliminar configuraciones de Elementor que contienen URLs externas
    content = re.sub(r'"urls":\{"assets":"https://maestrogregorio\.com/wp-content/plugins/elementor/assets/"', '"urls":{"assets":"wp-content/plugins/elementor/assets/"', content)
    content = re.sub(r'"rest":"https://maestrogregorio\.com/wp-json/"', '"rest":"wp-json/"', content)
    
    # Limpiar líneas vacías múltiples
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {file_path} limpiado")

def main():
    """Función principal"""
    base_dir = "/Users/edwarbechara/sitio_descargado/maestrogregorio.com"
    
    # Limpiar index.html
    index_file = os.path.join(base_dir, "index.html")
    if os.path.exists(index_file):
        clean_html_file(index_file)
    
    print("\n✅ Limpieza completada!")
    print("\nArchivos y directorios eliminados:")
    print("- xmlrpc.php y xmlrpc0db0.php")
    print("- Directorios: feed/, comments/, wp-json/")
    print("- Páginas de error: -negative.html, GET.html, etc.")
    print("- Directorios innecesarios: OPR/, Trident/, images/, etc.")
    print("\nReferencias externas eliminadas:")
    print("- Google Tag Manager y Analytics")
    print("- Google Fonts")
    print("- Scripts de chat externos")
    print("- URLs absolutas convertidas a relativas")

if __name__ == "__main__":
    main()