#!/usr/bin/env python3
"""
Cache Busting para Vercel
Fuerza la actualización de caché agregando versiones a todos los recursos
"""

import re
import os
import time
import hashlib

def force_cache_update(file_path):
    """Fuerza la actualización de caché en Vercel"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    print("🔄 Forzando actualización de caché en Vercel...")
    
    # Generar timestamp único para cache busting
    timestamp = str(int(time.time()))
    
    # 1. Actualizar todas las referencias CSS con nuevas versiones
    css_patterns = [
        r'(\?ver=[\d\.]+)',
        r'(\?ver=[\w\d\.]+)',
    ]
    
    for pattern in css_patterns:
        content = re.sub(pattern, f'?ver={timestamp}', content)
    
    # 2. Agregar cache busting a recursos específicos que están causando problemas
    problematic_resources = [
        'protection.js',
        'frontend-lite.min34a7.css',
        'jquery.minf43b.js',
        'base.min72ad.css',
        'chaty-front.min7bd6.css',
        'pa-frontend-dc36db04f.min8039.css',
        'fontawesome.min52d5.css',
        'wpforms-full.minbf90.css'
    ]
    
    for resource in problematic_resources:
        # Buscar y actualizar cada recurso problemático
        pattern = f'({re.escape(resource)}[^"]*)'
        def add_cache_buster(match):
            url = match.group(1)
            if '?' in url:
                return f"{url}&cb={timestamp}"
            else:
                return f"{url}?cb={timestamp}"
        
        content = re.sub(pattern, add_cache_buster, content)
    
    # 3. Agregar meta tag para forzar no-cache
    no_cache_meta = f'''
<!-- Cache Busting para Vercel -->
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="cache-version" content="{timestamp}">
'''
    
    # Insertar después del CSS crítico
    critical_css_end = content.find('</style>') + 8
    if critical_css_end > 7:
        content = content[:critical_css_end] + no_cache_meta + content[critical_css_end:]
    
    # 4. Actualizar el CSS crítico con una versión nueva
    critical_css_pattern = r'(<style id="critical-above-fold">)'
    content = re.sub(critical_css_pattern, f'<style id="critical-above-fold-v{timestamp}">', content)
    
    # 5. Agregar script para forzar reload de recursos
    force_reload_script = f'''
<script>
// Force cache update para Vercel - v{timestamp}
(function() {{
    'use strict';
    
    // Verificar si es la primera carga después de la optimización
    var cacheVersion = '{timestamp}';
    var lastVersion = localStorage.getItem('site-cache-version');
    
    if (lastVersion !== cacheVersion) {{
        console.log('🔄 Actualizando caché del sitio...');
        
        // Limpiar caché del navegador
        if ('caches' in window) {{
            caches.keys().then(function(names) {{
                names.forEach(function(name) {{
                    caches.delete(name);
                }});
            }});
        }}
        
        // Actualizar versión en localStorage
        localStorage.setItem('site-cache-version', cacheVersion);
        
        // Forzar recarga de CSS críticos
        var criticalStyles = document.querySelectorAll('link[rel="stylesheet"]');
        criticalStyles.forEach(function(link, index) {{
            setTimeout(function() {{
                var href = link.href;
                if (href.indexOf('cb=') === -1) {{
                    link.href = href + (href.indexOf('?') > -1 ? '&' : '?') + 'cb=' + cacheVersion;
                }}
            }}, index * 50);
        }});
    }}
    
    // Optimización adicional para Vercel
    window.addEventListener('load', function() {{
        // Precargar recursos críticos para la siguiente navegación
        var criticalResources = [
            'wp-content/themes/woodmart/css/parts/base.min72ad.css?cb={timestamp}',
            'wp-includes/js/jquery/jquery.minf43b.js?cb={timestamp}'
        ];
        
        criticalResources.forEach(function(resource) {{
            var link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = resource;
            document.head.appendChild(link);
        }});
    }});
}})();
</script>'''
    
    # Insertar script antes del cierre del body
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + force_reload_script + content[body_end:]
    
    # Escribir archivo actualizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ Cache busting aplicado!")
    print(f"🔢 Versión de caché: {timestamp}")
    print("📊 Cambios realizados:")
    print("   - Meta tags no-cache agregados")
    print("   - Versiones de recursos actualizadas")
    print("   - Script de limpieza de caché agregado")
    print("   - Cache busting para recursos problemáticos")
    print("   - Optimización específica para Vercel")

if __name__ == "__main__":
    html_file = "index.html"
    if os.path.exists(html_file):
        force_cache_update(html_file)
    else:
        print(f"❌ Error: No se encontró {html_file}")