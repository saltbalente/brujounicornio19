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

    // Bloquear selección de texto
    document.addEventListener('selectstart', function(e) {
        e.preventDefault();
        return false;
    });

    // Bloquear arrastrar elementos
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    });

    // Configurar protecciones cuando el DOM esté listo
    document.addEventListener('DOMContentLoaded', function() {
        // Deshabilitar selección con CSS
        if (document.body) {
            document.body.style.webkitUserSelect = 'none';
            document.body.style.mozUserSelect = 'none';
            document.body.style.msUserSelect = 'none';
            document.body.style.userSelect = 'none';
        }

        // Bloquear imágenes de ser guardadas
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

    // Detectar DevTools abierto
    var devtools = {
        open: false,
        orientation: null
    };

    var threshold = 160;

    setInterval(function() {
        if (window.outerHeight - window.innerHeight > threshold || 
            window.outerWidth - window.innerWidth > threshold) {
            if (!devtools.open) {
                devtools.open = true;
                // Redirigir o mostrar mensaje
                document.body.innerHTML = '<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#000;color:#fff;display:flex;align-items:center;justify-content:center;font-size:24px;z-index:999999;">Acceso no autorizado detectado</div>';
            }
        } else {
            devtools.open = false;
        }
    }, 500);

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