#!/usr/bin/env python3
"""
Script de Optimización de Rendimiento Web
Optimiza CSS, JS y recursos para mejorar LCP y FCP
"""

import re
import os
from pathlib import Path

def optimize_html_performance(file_path):
    """Optimiza el HTML para mejorar el rendimiento de carga"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    print("🚀 Iniciando optimización de rendimiento...")
    
    # 1. Identificar CSS crítico (above the fold)
    critical_css_patterns = [
        r'<link[^>]*href="[^"]*base\.min[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*bootstrap[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*header[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*frontend-lite\.min[^"]*\.css[^"]*"[^>]*>',
    ]
    
    # 2. Identificar CSS no crítico para diferir
    non_critical_css_patterns = [
        r'<link[^>]*href="[^"]*widget[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*woo-[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*mod-[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*opt-[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*chaty[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*premium-addons[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*essential-addons[^"]*\.css[^"]*"[^>]*>',
    ]
    
    # 3. Diferir CSS no crítico
    for pattern in non_critical_css_patterns:
        def defer_css(match):
            link_tag = match.group(0)
            # Cambiar rel="stylesheet" por rel="preload" as="style" onload="this.onload=null;this.rel='stylesheet'"
            if 'rel="stylesheet"' in link_tag:
                deferred = link_tag.replace(
                    'rel="stylesheet"',
                    'rel="preload" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"'
                )
                # Agregar noscript fallback
                noscript = f'<noscript>{link_tag}</noscript>'
                return deferred + noscript
            return link_tag
        
        content = re.sub(pattern, defer_css, content)
    
    # 4. Optimizar JavaScript - diferir scripts no críticos
    js_defer_patterns = [
        r'<script[^>]*src="[^"]*jquery-migrate[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*scrollBar[^"]*"[^>]*></script>',
        r'<script[^>]*src="[^"]*device[^"]*"[^>]*></script>',
    ]
    
    for pattern in js_defer_patterns:
        def defer_js(match):
            script_tag = match.group(0)
            if 'defer' not in script_tag and 'async' not in script_tag:
                return script_tag.replace('<script', '<script defer')
            return script_tag
        
        content = re.sub(pattern, defer_js, content)
    
    # 5. Agregar preload para recursos críticos
    head_end = content.find('</head>')
    if head_end != -1:
        preload_links = '''
<!-- Preload recursos críticos -->
<link rel="preload" href="wp-content/themes/woodmart/css/parts/base.min72ad.css" as="style">
<link rel="preload" href="wp-includes/js/jquery/jquery.minf43b.js" as="script">
<link rel="preload" href="wp-content/plugins/elementor/assets/css/frontend-lite.min34a7.css" as="style">
'''
        content = content[:head_end] + preload_links + content[head_end:]
    
    # 6. Agregar CSS crítico inline (básico)
    critical_css = '''
<style>
/* CSS Crítico Inline */
body{margin:0;padding:0;font-family:Arial,sans-serif}
.elementor-section{display:block}
.elementor-container{max-width:1200px;margin:0 auto;padding:0 15px}
.elementor-row{display:flex;flex-wrap:wrap}
.elementor-column{flex:1;padding:0 15px}
.elementor-widget{margin-bottom:20px}
.elementor-heading-title{margin:0 0 15px;font-weight:600}
.elementor-image img{max-width:100%;height:auto}
.elementor-button{display:inline-block;padding:12px 24px;text-decoration:none;border-radius:3px}
@media (max-width:767px){
.elementor-column{flex:100%;margin-bottom:20px}
.elementor-container{padding:0 10px}
}
</style>'''
    
    # Insertar CSS crítico antes del primer CSS externo
    first_css = re.search(r'<link[^>]*rel="stylesheet"[^>]*>', content)
    if first_css:
        content = content[:first_css.start()] + critical_css + content[first_css.start():]
    
    # 7. Optimizar carga de fuentes
    font_patterns = [
        r'<link[^>]*href="[^"]*fontawesome[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*elementor-icons[^"]*"[^>]*>',
    ]
    
    for pattern in font_patterns:
        def optimize_fonts(match):
            link_tag = match.group(0)
            if 'rel="stylesheet"' in link_tag:
                return link_tag.replace(
                    'rel="stylesheet"',
                    'rel="preload" as="style" onload="this.onload=null;this.rel=\'stylesheet\'" crossorigin'
                ) + f'<noscript>{link_tag}</noscript>'
            return link_tag
        
        content = re.sub(pattern, optimize_fonts, content)
    
    # 8. Agregar resource hints
    dns_prefetch = '''
<!-- DNS Prefetch para recursos externos -->
<link rel="dns-prefetch" href="//fonts.googleapis.com">
<link rel="dns-prefetch" href="//fonts.gstatic.com">
'''
    
    if head_end != -1:
        content = content[:head_end] + dns_prefetch + content[head_end:]
    
    # Escribir archivo optimizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ Optimización de rendimiento completada!")
    print("📊 Mejoras implementadas:")
    print("   - CSS no crítico diferido")
    print("   - JavaScript optimizado con defer")
    print("   - CSS crítico inline")
    print("   - Preload de recursos importantes")
    print("   - Resource hints agregados")
    print("   - Fuentes optimizadas")

if __name__ == "__main__":
    html_file = "index.html"
    if os.path.exists(html_file):
        optimize_html_performance(html_file)
    else:
        print(f"❌ Error: No se encontró {html_file}")