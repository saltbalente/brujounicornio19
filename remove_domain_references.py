#!/usr/bin/env python3
"""
Script para eliminar todas las referencias al dominio maestrogregorio.com
y hacer el sitio completamente independiente
"""

import re
import os

def clean_domain_references(file_path):
    """Limpia todas las referencias al dominio maestrogregorio.com"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Contador de cambios
    changes = 0
    
    # 1. Eliminar enlaces oEmbed (incluyendo URLs codificadas)
    oembed_patterns = [
        r'<link rel="alternate"[^>]*oembed[^>]*maestrogregorio\.com[^>]*>',
        r'<link rel="alternate"[^>]*href="[^"]*maestrogregorio\.com[^"]*"[^>]*>',
        r'href="[^"]*maestrogregorio\.com[^"]*"'
    ]
    
    for pattern in oembed_patterns:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, '', content)
            changes += len(matches)
            print(f"✅ Eliminadas {len(matches)} referencias oEmbed")
    
    # Eliminar URLs codificadas específicamente
    encoded_patterns = [
        r'url=https%3A%2F%2Fmaestrogregorio\.com[^"&]*',
        r'https%3A%2F%2Fmaestrogregorio\.com[^"&]*'
    ]
    
    for pattern in encoded_patterns:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, '', content)
            changes += len(matches)
            print(f"✅ Eliminadas {len(matches)} URLs codificadas")
    
    # 2. Reemplazar URL de video de fondo con ruta local
    video_pattern = r'https://maestrogregorio\.com/wp-content/uploads/([^"]*\.mp4)'
    if re.search(video_pattern, content):
        content = re.sub(video_pattern, r'wp-content/uploads/\1', content)
        changes += len(re.findall(video_pattern, content))
        print("✅ Convertida URL de video a ruta local")
    
    # 3. Reemplazar URLs de AJAX con rutas relativas o eliminar
    ajax_patterns = [
        # AJAX URLs en configuraciones JavaScript (con barras escapadas)
        (r'"ajaxurl":"https:\\/\\/maestrogregorio\.com\\/wp-admin\\/admin-ajax\.php"', '"ajaxurl":"#"'),
        (r'"https:\\/\\/maestrogregorio\.com\\/wp-admin\\/admin-ajax\.php"', '"#"'),
        
        # URLs de assets (con barras escapadas)
        (r'"assets":"https:\\/\\/maestrogregorio\.com\\/wp-content\\/plugins\\/([^"]*)"', r'"assets":"wp-content\/plugins\/\1"'),
        (r'"rest":"https:\\/\\/maestrogregorio\.com\\/wp-json\\/"', '"rest":"#"'),
        
        # URLs de animaciones y otros recursos (con barras escapadas)
        (r'"https:\\/\\/maestrogregorio\.com\\/wp-content\\/plugins\\/([^"]*)"', r'"wp-content\/plugins\/\1"'),
        
        # Permalink de página (con barras escapadas)
        (r'"page_permalink":"https:\\/\\/maestrogregorio\.com\\/"', '"page_permalink":"./"'),
        
        # Featured image (con barras escapadas)
        (r'"featuredImage":"https:\\/\\/maestrogregorio\.com\\/wp-content\\/uploads\\/([^"]*)"', r'"featuredImage":"wp-content\/uploads\/\1"'),
        
        # URLs en configuraciones de Elementor (con barras escapadas)
        (r'"urls":{"assets":"https:\\/\\/maestrogregorio\.com\\/wp-content\\/plugins\\/elementor\\/assets\\/"', r'"urls":{"assets":"wp-content\/plugins\/elementor\/assets\/"'),
        
        # URLs de animaciones por defecto (con barras escapadas)
        (r'"defaultAnimationUrl":"https:\\/\\/maestrogregorio\.com\\/wp-content\\/plugins\\/([^"]*)"', r'"defaultAnimationUrl":"wp-content\/plugins\/\1"'),
        
        # URLs en data-settings de elementos (con barras escapadas y codificadas)
        (r'&quot;background_video_link&quot;:&quot;https:\\/\\/maestrogregorio\.com\\/wp-content\\/uploads\\/([^&]*)&quot;', r'&quot;background_video_link&quot;:&quot;wp-content\/uploads\/\1&quot;'),
        
        # Home URL en configuraciones JavaScript
        (r'"home_url":"https:\\/\\/maestrogregorio\.com\\/"', '"home_url":"./"'),
        
        # URLs en configuraciones CSS y JS específicas
        (r'"vimeo_library_url":"https:\\/\\/maestrogregorio\.com\\/([^"]*)"', r'"vimeo_library_url":"\1"'),
        
        # URLs en arrays de CSS y themes
        (r'"https:\\/\\/maestrogregorio\.com\\/wp-content\\/themes\\/([^"]*)"', r'"wp-content\/themes\/\1"'),
        
        # URLs en arrays de estilos de iframe
        (r'"https:\\/\\/maestrogregorio\\.com\\/wp-includes\\/([^"]*)"\'', r'"wp-includes\/\1"'),
        
        # URLs sin protocolo que empiezan con index.html// (con barras escapadas)
        (r'"index\.html\\/\\/maestrogregorio\.com\\/([^"]*)"', r'"\1"'),
    ]
    
    for pattern, replacement in ajax_patterns:
        if re.search(pattern, content):
            old_content = content
            content = re.sub(pattern, replacement, content)
            pattern_changes = len(re.findall(pattern, old_content))
            changes += pattern_changes
            if pattern_changes > 0:
                print(f"✅ Reemplazadas {pattern_changes} referencias de AJAX/assets")
    
    # 4. Eliminar cualquier referencia restante al dominio
    remaining_pattern = r'https://maestrogregorio\.com[^"\s]*'
    remaining_matches = re.findall(remaining_pattern, content)
    if remaining_matches:
        print(f"⚠️  Encontradas {len(remaining_matches)} referencias adicionales:")
        for match in remaining_matches[:5]:  # Mostrar solo las primeras 5
            print(f"   - {match}")
        
        # Reemplazar con rutas relativas cuando sea posible
        content = re.sub(r'https://maestrogregorio\.com/wp-content/', 'wp-content/', content)
        content = re.sub(r'https://maestrogregorio\.com/', './', content)
        changes += len(remaining_matches)
    
    # Escribir el archivo actualizado
    if changes > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Archivo actualizado con {changes} cambios")
    else:
        print("ℹ️  No se encontraron referencias al dominio")
    
    return changes

def main():
    """Función principal"""
    base_dir = "/Users/edwarbechara/sitio_descargado/maestrogregorio.com"
    index_file = os.path.join(base_dir, "index.html")
    
    print("🧹 Limpiando referencias al dominio maestrogregorio.com...")
    print("=" * 60)
    
    if os.path.exists(index_file):
        total_changes = clean_domain_references(index_file)
        print("=" * 60)
        print(f"✅ Proceso completado. Total de cambios: {total_changes}")
        
        # Verificar que no queden referencias
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        remaining = len(re.findall(r'maestrogregorio\.com', content))
        if remaining == 0:
            print("🎉 ¡Sitio completamente independiente! No quedan referencias al dominio original.")
        else:
            print(f"⚠️  Aún quedan {remaining} referencias al dominio original.")
    else:
        print(f"❌ No se encontró el archivo: {index_file}")

if __name__ == "__main__":
    main()