#!/usr/bin/env python3
"""
Script Avanzado de Optimización de Rendimiento
Implementa técnicas avanzadas para reducir el tiempo de bloqueo de renderizado
"""

import re
import os

def advanced_performance_optimization(file_path):
    """Aplica optimizaciones avanzadas de rendimiento"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    print("🔧 Aplicando optimizaciones avanzadas...")
    
    # 1. Crear un bundle CSS crítico más completo
    advanced_critical_css = '''
<style>
/* CSS Crítico Avanzado - Above the Fold */
*{box-sizing:border-box}
body,html{margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.6}
.elementor-section{position:relative;overflow:hidden}
.elementor-container{max-width:1200px;margin:0 auto;padding:0 15px;position:relative}
.elementor-row{display:flex;flex-wrap:wrap;align-items:stretch}
.elementor-column{position:relative;min-height:1px;display:flex;flex-direction:column}
.elementor-column-gap-default>.elementor-column>.elementor-element-populated{padding:10px}
.elementor-widget{position:relative}
.elementor-widget:not(:last-child){margin-bottom:20px}
.elementor-heading-title{margin:0 0 15px;color:#333;font-weight:600;line-height:1.2}
.elementor-image{text-align:center}
.elementor-image img{border:none;border-radius:0;max-width:100%;height:auto;display:inline-block;vertical-align:middle}
.elementor-button-wrapper{text-align:left}
.elementor-button{font-family:inherit;font-size:inherit;line-height:1;fill:#fff;color:#fff;text-align:center;transition:all .3s;border:none;outline:none;cursor:pointer;text-decoration:none;display:inline-block;padding:12px 24px;background-color:#61ce70;border-radius:3px}
.elementor-button:hover{background-color:#4cae4c;transform:translateY(-1px)}
.elementor-widget-image-carousel{position:relative}
.swiper-container{margin:0 auto;position:relative;overflow:hidden;list-style:none;padding:0;z-index:1}
.swiper-wrapper{position:relative;width:100%;height:100%;z-index:1;display:flex;transition-property:transform;box-sizing:content-box}
.swiper-slide{flex-shrink:0;width:100%;height:100%;position:relative;transition-property:transform}
.swiper-slide img{width:100%;height:auto;object-fit:cover}
.swiper-button-next,.swiper-button-prev{position:absolute;top:50%;width:27px;height:44px;margin-top:-22px;z-index:10;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#007cba;background:rgba(255,255,255,.8);border-radius:3px;transition:all .3s}
.swiper-button-prev{left:10px}
.swiper-button-next{right:10px}
.swiper-button-next:hover,.swiper-button-prev:hover{background:rgba(255,255,255,.95);transform:scale(1.1)}
@media (max-width:1024px){
.elementor-column{flex:50%;max-width:50%}
}
@media (max-width:767px){
.elementor-column{flex:100%;max-width:100%;margin-bottom:20px}
.elementor-container{padding:0 10px}
.elementor-button{padding:10px 20px;font-size:14px}
.swiper-button-next,.swiper-button-prev{width:24px;height:40px;margin-top:-20px}
}
@media (max-width:480px){
.elementor-container{padding:0 5px}
.elementor-heading-title{font-size:1.5em}
.swiper-button-next,.swiper-button-prev{display:none}
}
/* Optimización de carga de imágenes */
img{loading:lazy}
.elementor-image img{transition:opacity .3s ease;opacity:0}
.elementor-image img.loaded{opacity:1}
/* Skeleton loading para mejor UX */
.skeleton{background:linear-gradient(90deg,#f0f0f0 25%,#e0e0e0 50%,#f0f0f0 75%);background-size:200% 100%;animation:loading 1.5s infinite}
@keyframes loading{0%{background-position:200% 0}100%{background-position:-200% 0}}
</style>'''
    
    # Reemplazar el CSS crítico anterior con el avanzado
    content = re.sub(r'<style>\s*/\* CSS Crítico Inline \*/.*?</style>', advanced_critical_css, content, flags=re.DOTALL)
    
    # 2. Optimizar la carga de jQuery (crítico)
    jquery_pattern = r'<script[^>]*src="[^"]*jquery\.min[^"]*"[^>]*></script>'
    def optimize_jquery(match):
        script_tag = match.group(0)
        # Mantener jQuery como crítico pero optimizado
        return script_tag.replace('<script', '<script defer')
    
    content = re.sub(jquery_pattern, optimize_jquery, content)
    
    # 3. Agregar script de carga inteligente de imágenes
    image_loading_script = '''
<script>
// Carga inteligente de imágenes y optimización de rendimiento
(function() {
    'use strict';
    
    // Lazy loading mejorado para imágenes
    function initLazyLoading() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px'
            });
            
            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback para navegadores sin IntersectionObserver
            images.forEach(img => img.classList.add('loaded'));
        }
    }
    
    // Optimización de Web Vitals
    function optimizeWebVitals() {
        // Preconectar a dominios externos
        const preconnectDomains = ['fonts.googleapis.com', 'fonts.gstatic.com'];
        preconnectDomains.forEach(domain => {
            const link = document.createElement('link');
            link.rel = 'preconnect';
            link.href = `https://${domain}`;
            link.crossOrigin = 'anonymous';
            document.head.appendChild(link);
        });
        
        // Optimizar CLS (Cumulative Layout Shift)
        const images = document.querySelectorAll('img:not([width]):not([height])');
        images.forEach(img => {
            img.style.aspectRatio = '16/9'; // Ratio por defecto
        });
    }
    
    // Carga diferida de recursos no críticos
    function loadNonCriticalResources() {
        // Cargar CSS diferido después del LCP
        const deferredStyles = document.querySelectorAll('link[rel="preload"][as="style"]');
        deferredStyles.forEach(link => {
            if (link.onload === null) {
                link.onload = function() {
                    this.onload = null;
                    this.rel = 'stylesheet';
                };
            }
        });
    }
    
    // Inicialización optimizada
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initLazyLoading();
            optimizeWebVitals();
            
            // Cargar recursos no críticos después de un delay
            setTimeout(loadNonCriticalResources, 100);
        });
    } else {
        initLazyLoading();
        optimizeWebVitals();
        loadNonCriticalResources();
    }
    
    // Optimización del slider personalizado
    window.addEventListener('load', function() {
        if (typeof initCustomSlider === 'function') {
            initCustomSlider();
        }
    });
})();
</script>'''
    
    # Insertar el script antes del cierre del body
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + image_loading_script + content[body_end:]
    
    # 4. Optimizar más CSS no crítico
    additional_defer_patterns = [
        r'<link[^>]*href="[^"]*swiper[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*wpforms[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*brands\.min[^"]*\.css[^"]*"[^>]*>',
        r'<link[^>]*href="[^"]*solid\.min[^"]*\.css[^"]*"[^>]*>',
    ]
    
    for pattern in additional_defer_patterns:
        def defer_additional_css(match):
            link_tag = match.group(0)
            if 'rel="stylesheet"' in link_tag and 'preload' not in link_tag:
                deferred = link_tag.replace(
                    'rel="stylesheet"',
                    'rel="preload" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"'
                )
                return deferred + f'<noscript>{link_tag}</noscript>'
            return link_tag
        
        content = re.sub(pattern, defer_additional_css, content)
    
    # 5. Agregar meta tags de optimización
    head_end = content.find('</head>')
    if head_end != -1:
        optimization_meta = '''
<!-- Optimización de rendimiento -->
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
'''
        content = content[:head_end] + optimization_meta + content[head_end:]
    
    # Escribir archivo optimizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ Optimizaciones avanzadas aplicadas!")
    print("📈 Mejoras adicionales:")
    print("   - CSS crítico avanzado con skeleton loading")
    print("   - Lazy loading inteligente de imágenes")
    print("   - Optimización de Web Vitals (CLS, LCP)")
    print("   - Carga diferida mejorada")
    print("   - Preconexiones optimizadas")
    print("   - Meta tags de rendimiento")

if __name__ == "__main__":
    html_file = "index.html"
    if os.path.exists(html_file):
        advanced_performance_optimization(html_file)
    else:
        print(f"❌ Error: No se encontró {html_file}")