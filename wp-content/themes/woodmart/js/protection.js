/**
 * Script de Protección del Sitio Web
 * Bloquea funciones de copia y acceso al código fuente
 */

(function() {
    'use strict';

    // Bloquear clic derecho
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });

    // Bloquear teclas de acceso rápido
    document.addEventListener('keydown', function(e) {
        // F12 (DevTools)
        if (e.keyCode === 123) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+Shift+I (DevTools)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+Shift+J (Console)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+U (Ver código fuente)
        if (e.ctrlKey && e.keyCode === 85) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+S (Guardar página)
        if (e.ctrlKey && e.keyCode === 83) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+A (Seleccionar todo)
        if (e.ctrlKey && e.keyCode === 65) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+C (Copiar)
        if (e.ctrlKey && e.keyCode === 67) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+V (Pegar)
        if (e.ctrlKey && e.keyCode === 86) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+X (Cortar)
        if (e.ctrlKey && e.keyCode === 88) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+P (Imprimir)
        if (e.ctrlKey && e.keyCode === 80) {
            e.preventDefault();
            return false;
        }
    });

    // Bloquear selección de texto (solo en desktop)
    if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        document.addEventListener('selectstart', function(e) {
            // Permitir selección en campos de formulario
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return true;
            }
            e.preventDefault();
            return false;
        });
    }

    // Bloquear arrastrar elementos
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    });

    // Configurar protecciones cuando el DOM esté listo
    document.addEventListener('DOMContentLoaded', function() {
        // Deshabilitar selección con CSS (solo en desktop)
        if (document.body && !/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            document.body.style.webkitUserSelect = 'none';
            document.body.style.mozUserSelect = 'none';
            document.body.style.msUserSelect = 'none';
            document.body.style.userSelect = 'none';
        }

        // Bloquear imágenes de ser guardadas (solo en desktop)
        if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            var images = document.getElementsByTagName('img');
            for (var i = 0; i < images.length; i++) {
                images[i].addEventListener('dragstart', function(e) {
                    e.preventDefault();
                    return false;
                });
                images[i].style.webkitUserSelect = 'none';
                images[i].style.mozUserSelect = 'none';
                images[i].style.msUserSelect = 'none';
                images[i].style.userSelect = 'none';
            }
        }

        // Eliminar comentarios del DOM
        var walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_COMMENT,
            null,
            false
        );
        
        var commentsToRemove = [];
        var node;
        
        while (node = walker.nextNode()) {
            commentsToRemove.push(node);
        }
        
        commentsToRemove.forEach(function(comment) {
            comment.parentNode.removeChild(comment);
        });
    });

    // Detectar DevTools abierto (solo en desktop)
    var devtools = {
        open: false,
        orientation: null
    };

    var threshold = 160;

    // Solo aplicar detección de DevTools en dispositivos de escritorio
    if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        setInterval(function() {
            // Solo activar si la diferencia es muy grande (más de 300px)
            if ((window.outerHeight - window.innerHeight > 300 || 
                window.outerWidth - window.innerWidth > 300) && 
                window.innerWidth > 1024) { // Solo en pantallas grandes
                if (!devtools.open) {
                    devtools.open = true;
                    // Mostrar advertencia menos agresiva
                    var warning = document.createElement('div');
                    warning.style.cssText = 'position:fixed;top:20px;right:20px;background:rgba(255,0,0,0.9);color:#fff;padding:15px;border-radius:5px;z-index:999999;font-size:14px;max-width:300px;';
                    warning.innerHTML = '⚠️ Herramientas de desarrollador detectadas';
                    document.body.appendChild(warning);
                    
                    setTimeout(function() {
                        if (warning.parentNode) {
                            warning.parentNode.removeChild(warning);
                        }
                        devtools.open = false;
                    }, 3000);
                }
            }
        }, 1000); // Reducir frecuencia de verificación
    }

    // Bloquear console.log y otras funciones de consola
    if (typeof console !== 'undefined') {
        console.log = function() {};
        console.warn = function() {};
        console.error = function() {};
        console.info = function() {};
        console.debug = function() {};
        console.clear = function() {};
        console.dir = function() {};
        console.dirxml = function() {};
        console.table = function() {};
        console.trace = function() {};
        console.group = function() {};
        console.groupCollapsed = function() {};
        console.groupEnd = function() {};
        console.time = function() {};
        console.timeEnd = function() {};
        console.profile = function() {};
        console.profileEnd = function() {};
        console.count = function() {};
    }

    // Bloquear herramientas de inspección
    document.addEventListener('keyup', function(e) {
        if (e.keyCode === 123) { // F12
            e.preventDefault();
            return false;
        }
    });

    // Mensaje de advertencia en consola
    setTimeout(function() {
        if (typeof console !== 'undefined') {
            console.clear();
        }
    }, 1000);

})();