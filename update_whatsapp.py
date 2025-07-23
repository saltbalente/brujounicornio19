#!/usr/bin/env python3
"""
Script para reemplazar todos los enlaces de WhatsApp con el número de Estados Unidos
y mensaje personalizado
"""

import re
import os

def replace_whatsapp_links(file_path):
    """Reemplaza todos los enlaces de WhatsApp en el archivo"""
    print(f"Actualizando enlaces de WhatsApp en {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Número de Estados Unidos y mensaje personalizado
    us_number = "13853137278"
    message = "Quiero una consulta con el Unicornio Negro"
    
    # URL codificada para WhatsApp
    encoded_message = message.replace(" ", "%20")
    new_whatsapp_url = f"https://wa.me/{us_number}?text={encoded_message}"
    
    # Reemplazar todos los enlaces wa.me con diferentes números colombianos
    content = re.sub(r'https://wa\.me/573\d+(?:\?text=[^"]*)?', new_whatsapp_url, content)
    
    # También reemplazar cualquier otro formato de wa.me que pueda existir
    content = re.sub(r'https://wa\.me/\d+(?:\?text=[^"]*)?', new_whatsapp_url, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Enlaces de WhatsApp actualizados")
    print(f"✓ Nuevo número: +{us_number}")
    print(f"✓ Mensaje: {message}")

def main():
    """Función principal"""
    base_dir = "/Users/edwarbechara/sitio_descargado/maestrogregorio.com"
    
    # Actualizar index.html
    index_file = os.path.join(base_dir, "index.html")
    if os.path.exists(index_file):
        replace_whatsapp_links(index_file)
    
    print("\n✅ Actualización de WhatsApp completada!")
    print(f"Todos los enlaces ahora apuntan a: +1 (385) 313-7278")
    print(f"Con el mensaje: 'Quiero una consulta con el Unicornio Negro'")

if __name__ == "__main__":
    main()