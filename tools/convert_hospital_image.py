#!/usr/bin/env python3
"""Convert hospital building image to multiple optimized formats"""
from PIL import Image
import os
import sys

BASE_DIR = r"D:\minimax\New folder\Green Hospital Ltd"
source = os.path.join(BASE_DIR, 'images', 'hospital-building-real.webp')

img = Image.open(source)
print(f"Original size: {os.path.getsize(source)/1024:.1f} KB")
print(f"Original dimensions: {img.size}")

# Convert to JPG (universal compatibility, smaller file)
img_rgb = img.convert('RGB')
jpg_path = os.path.join(BASE_DIR, 'images', 'about-hospital.jpg')
img_rgb.save(jpg_path, 'JPEG', quality=85, optimize=True)
print(f"JPG saved: {os.path.getsize(jpg_path)/1024:.1f} KB")

# Convert to PNG (lossless)
png_path = os.path.join(BASE_DIR, 'images', 'about-hospital.png')
img.save(png_path, 'PNG', optimize=True)
print(f"PNG saved: {os.path.getsize(png_path)/1024:.1f} KB")

# Create a smaller compressed version for fast loading
img_small = img_rgb.copy()
img_small.thumbnail((1200, 800), Image.Resampling.LANCZOS)
sm_path = os.path.join(BASE_DIR, 'images', 'about-hospital-sm.jpg')
img_small.save(sm_path, 'JPEG', quality=80, optimize=True, progressive=True)
print(f"Small JPG: {os.path.getsize(sm_path)/1024:.1f} KB")

# Also create a banner-style version for hero
img_hero = img_rgb.copy()
img_hero.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
hero_path = os.path.join(BASE_DIR, 'images', 'hospital-building-hero.jpg')
img_hero.save(hero_path, 'JPEG', quality=82, optimize=True, progressive=True)
print(f"Hero JPG: {os.path.getsize(hero_path)/1024:.1f} KB")

print("\nAll variants created successfully!")
