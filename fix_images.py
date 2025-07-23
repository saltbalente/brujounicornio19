#!/usr/bin/env python3
"""
Script para limpiar los srcset de imágenes y dejar solo las que existen
"""

import re
import os
from pathlib import Path

def get_existing_images(base_dir):
    """Obtiene una lista de todas las imágenes que existen"""
    uploads_dir = Path(base_dir) / "wp-content" / "uploads"
    existing_images = set()
    
    for img_file in uploads_dir.rglob("*"):
        if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
            # Obtener la ruta relativa desde el directorio base
            rel_path = img_file.relative_to(base_dir)
            existing_images.add(str(rel_path))
    
    return existing_images

def clean_srcset(content, existing_images):
    """Limpia los srcset dejando solo las imágenes que existen"""
    
    def clean_srcset_attribute(match):
        full_match = match.group(0)
        srcset_content = match.group(1)
        
        # Dividir el srcset en elementos individuales
        srcset_items = [item.strip() for item in srcset_content.split(',')]
        valid_items = []
        
        for item in srcset_items:
            if item:
                # Extraer la URL de la imagen (antes del espacio y el descriptor de ancho)
                parts = item.strip().split()
                if parts:
                    img_path = parts[0]
                    if img_path in existing_images:
                        valid_items.append(item)
        
        if valid_items:
            new_srcset = ', '.join(valid_items)
            return full_match.replace(srcset_content, new_srcset)
        else:
            # Si no hay elementos válidos, eliminar el atributo srcset
            return re.sub(r'\s*srcset="[^"]*"', '', full_match)
    
    # Buscar y limpiar todos los srcset
    content = re.sub(r'srcset="([^"]*)"', clean_srcset_attribute, content)
    
    return content

def fix_image_sources(content, existing_images):
    """Verifica que las imágenes en src existan, si no, busca alternativas"""
    
    def fix_src_attribute(match):
        full_match = match.group(0)
        src_path = match.group(1)
        
        if src_path in existing_images:
            return full_match
        
        # Buscar una imagen similar que exista
        base_name = Path(src_path).stem
        base_dir = str(Path(src_path).parent)
        
        for existing_img in existing_images:
            if base_name in existing_img and base_dir in existing_img:
                return full_match.replace(src_path, existing_img)
        
        return full_match
    
    # Buscar y corregir todos los src
    content = re.sub(r'src="([^"]*)"', fix_src_attribute, content)
    
    return content

def main():
    """Función principal"""
    base_dir = "/Users/edwarbechara/sitio_descargado/maestrogregorio.com"
    
    print("🔍 Escaneando imágenes existentes...")
    existing_images = get_existing_images(base_dir)
    print(f"✓ Encontradas {len(existing_images)} imágenes")
    
    # Limpiar index.html
    index_file = os.path.join(base_dir, "index.html")
    if os.path.exists(index_file):
        print(f"\n🧹 Limpiando {index_file}...")
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Limpiar srcset
        content = clean_srcset(content, existing_images)
        
        # Corregir src
        content = fix_image_sources(content, existing_images)
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {index_file} limpiado")
    
    print("\n✅ Limpieza de imágenes completada!")
    print("- Srcset limpiados para incluir solo imágenes existentes")
    print("- Referencias de src corregidas")

if __name__ == "__main__":
    main()