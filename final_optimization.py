#!/usr/bin/env python3
"""
Optimización Final de Dependencias
Asegura la carga correcta de jQuery y optimiza el orden de scripts
"""

import re
import os

def final_dependency_optimization(file_path):
    """Optimiza las dependencias finales para asegurar funcionamiento correcto"""
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    print("🔧 Optimizando dependencias finales...")
    
    # 1. Asegurar que jQuery se carga antes que otros scripts que lo necesitan
    # Mover jQuery al head para carga inmediata
    jquery_pattern = r'<script src="wp-includes/js/jquery/jquery\.minf43b\.js[^"]*"[^>]*></script>'
    jquery_match = re.search(jquery_pattern, content)
    
    if jquery_match:
        jquery_script = jquery_match.group(0)
        # Remover jQuery de su posición actual
        content = re.sub(jquery_pattern, '', content)
        
        # Insertar jQuery en el head, después del CSS crítico
        head_insertion_point = content.find('</style>') + 8  # Después del CSS crítico
        if head_insertion_point > 7:
            content = content[:head_insertion_point] + '\n' + jquery_script + '\n' + content[head_insertion_point:]
    
    # 2. Optimizar jQuery Migrate para carga diferida pero sin async
    content = re.sub(
        r'<script src="([^"]*jquery-migrate[^"]*)" defer async></script>',
        r'<script src="\1" defer></script>',
        content
    )
    
    # 3. Agregar script de inicialización optimizada
    initialization_script = '''
<script>
// Inicialización optimizada de dependencias
(function() {
    'use strict';
    
    // Verificar que jQuery esté disponible
    function waitForjQuery(callback) {
        if (typeof jQuery !== 'undefined') {
            callback();
        } else {
            setTimeout(function() {
                waitForjQuery(callback);
            }, 50);
        }
    }
    
    // Inicialización cuando jQuery esté listo
    waitForjQuery(function() {
        // Configurar jQuery para mejor rendimiento
        jQuery.ajaxSetup({
            cache: true
        });
        
        // Optimizar eventos de scroll
        var scrollTimer = null;
        jQuery(window).on('scroll', function() {
            if (scrollTimer) {
                clearTimeout(scrollTimer);
            }
            scrollTimer = setTimeout(function() {
                // Eventos de scroll optimizados
                jQuery(window).trigger('scroll.optimized');
            }, 16); // ~60fps
        });
        
        // Lazy loading mejorado para elementos dinámicos
        function initDynamicLazyLoading() {
            if ('IntersectionObserver' in window) {
                var lazyElements = document.querySelectorAll('[data-lazy]');
                var lazyObserver = new IntersectionObserver(function(entries) {
                    entries.forEach(function(entry) {
                        if (entry.isIntersecting) {
                            var element = entry.target;
                            if (element.dataset.lazy === 'image') {
                                var img = element.querySelector('img');
                                if (img && img.dataset.src) {
                                    img.src = img.dataset.src;
                                    img.classList.add('loaded');
                                }
                            }
                            lazyObserver.unobserve(element);
                        }
                    });
                }, {
                    rootMargin: '50px 0px'
                });
                
                lazyElements.forEach(function(element) {
                    lazyObserver.observe(element);
                });
            }
        }
        
        // Inicializar cuando el DOM esté listo
        jQuery(document).ready(function($) {
            initDynamicLazyLoading();
            
            // Optimizar formularios
            $('form').each(function() {
                var $form = $(this);
                $form.on('submit', function() {
                    $form.find('input[type="submit"], button[type="submit"]').prop('disabled', true);
                });
            });
            
            // Optimizar imágenes del slider
            $('.swiper-slide img').each(function(index) {
                var $img = $(this);
                if (index < 2) {
                    $img.attr('loading', 'eager');
                    $img.attr('fetchpriority', 'high');
                } else {
                    $img.attr('loading', 'lazy');
                }
            });
        });
    });
    
    // Optimización de Web Vitals
    function optimizeWebVitals() {
        // Reducir CLS (Cumulative Layout Shift)
        var images = document.querySelectorAll('img:not([width]):not([height])');
        images.forEach(function(img) {
            if (!img.style.aspectRatio) {
                img.style.aspectRatio = '16/9';
            }
        });
        
        // Optimizar LCP (Largest Contentful Paint)
        var heroElements = document.querySelectorAll('.elementor-section:first-child img, .swiper-slide:first-child img');
        heroElements.forEach(function(element) {
            element.setAttribute('fetchpriority', 'high');
            element.setAttribute('loading', 'eager');
        });
    }
    
    // Ejecutar optimizaciones
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', optimizeWebVitals);
    } else {
        optimizeWebVitals();
    }
})();
</script>'''
    
    # Insertar script después de jQuery
    jquery_end = content.find('<script src="wp-includes/js/jquery/jquery.minf43b.js') 
    if jquery_end != -1:
        script_end = content.find('</script>', jquery_end) + 9
        content = content[:script_end] + initialization_script + content[script_end:]
    
    # 4. Optimizar el orden de carga de CSS crítico vs no crítico
    # Asegurar que el CSS crítico esté al principio
    critical_css_pattern = r'<style id="critical-above-fold">.*?</style>'
    critical_css_match = re.search(critical_css_pattern, content, re.DOTALL)
    
    if critical_css_match:
        critical_css = critical_css_match.group(0)
        # Remover CSS crítico de su posición actual
        content = re.sub(critical_css_pattern, '', content, flags=re.DOTALL)
        
        # Insertar CSS crítico inmediatamente después de <head>
        head_start = content.find('<head>') + 6
        content = content[:head_start] + '\n' + critical_css + '\n' + content[head_start:]
    
    # 5. Agregar resource hints optimizados
    resource_hints = '''
<!-- Resource Hints Optimizados -->
<link rel="dns-prefetch" href="//fonts.googleapis.com">
<link rel="dns-prefetch" href="//fonts.gstatic.com">
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
'''
    
    # Insertar resource hints después del CSS crítico
    critical_css_end = content.find('</style>') + 8
    if critical_css_end > 7:
        content = content[:critical_css_end] + resource_hints + content[critical_css_end:]
    
    # Escribir archivo optimizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ Optimización final de dependencias completada!")
    print("🎯 Mejoras implementadas:")
    print("   - jQuery cargado inmediatamente en el head")
    print("   - Script de inicialización optimizada")
    print("   - Lazy loading dinámico mejorado")
    print("   - Optimización de Web Vitals (CLS, LCP)")
    print("   - Resource hints optimizados")
    print("   - Orden de carga optimizado")
    print("📊 Resultado esperado: Funcionalidad completa + rendimiento optimizado")

if __name__ == "__main__":
    html_file = "index.html"
    if os.path.exists(html_file):
        final_dependency_optimization(html_file)
    else:
        print(f"❌ Error: No se encontró {html_file}")