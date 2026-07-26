#!/usr/bin/env python3
"""Update remaining files with new logo patterns"""
import os
from pathlib import Path

BASE_DIR = Path(r"D:\minimax\New folder\Green Hospital Ltd")

# Replacements for doctor pages - no width/height
DOCTOR_REPLACEMENTS = [
    (
        '<link rel="icon" type="image/jpeg" href="../images/logo.jpg">',
        '<link rel="icon" type="image/png" sizes="32x32" href="../images/favicon-32.png">\n    <link rel="icon" type="image/png" sizes="16x16" href="../images/favicon-16.png">\n    <link rel="shortcut icon" href="../images/favicon-32.png">'
    ),
    (
        '<img src="../images/logo.jpg" alt="Faridpur Green Hospital Ltd Logo" onerror="this.onerror=null; this.src=\'https://placehold.co/200x60?text=Green+Hospital\';">',
        '<img src="../images/logo.png" alt="Faridpur Green Hospital Ltd Official Logo" width="240" height="100" onerror="this.onerror=null; this.src=\'../images/logo-official.jpg\';">'
    ),
    (
        '<img src="../images/logo.jpg" alt="Logo" class="footer-logo" onerror="this.onerror=null; this.src=\'https://placehold.co/200x60?text=Logo\';">',
        '<img src="../images/logo.png" alt="Faridpur Green Hospital Ltd Official Logo" class="footer-logo" width="240" height="100" onerror="this.onerror=null; this.src=\'../images/logo-official.jpg\';">'
    ),
    # Schema.org logo URL
    (
        '"logo": "https://greenhospitalbd.com/images/logo.jpg"',
        '"logo": "https://greenhospitalbd.com/images/logo.png"'
    ),
    (
        '"image": "https://greenhospitalbd.com/images/hospital-hero.jpg"',
        '"image": "https://greenhospitalbd.com/images/og-image.png"'
    ),
    (
        '<meta property="og:image" content="https://greenhospitalbd.com/images/hospital-hero.jpg">',
        '<meta property="og:image" content="https://greenhospitalbd.com/images/og-image.png">'
    ),
    (
        '<meta name="twitter:image" content="https://greenhospitalbd.com/images/hospital-hero.jpg">',
        '<meta name="twitter:image" content="https://greenhospitalbd.com/images/og-image.png">'
    ),
]

# Replacements for admin/login.html - has a different onerror
ADMIN_LOGIN_REPLACEMENTS = [
    (
        '<img src="../images/logo.jpg" alt="Logo" onerror="this.style.background=\'linear-gradient(135deg,#0a8d4a,#076835)\'; this.style.color=\'white\'; this.style.display=\'flex\'; this.style.alignItems=\'center\'; this.style.justifyContent=\'center\'; this.style.fontSize=\'1.5rem\'; this.style.fontWeight=\'bold\'; this.textContent=\'GH\';">',
        '<img src="../images/logo.png" alt="Faridpur Green Hospital Ltd Official Logo" width="240" height="100" onerror="this.onerror=null; this.src=\'../images/logo-official.jpg\';">'
    ),
]

# 404 page - needs full content update (no logo currently)
# We'll add one

def update_file(filepath, replacements, label):
    full_path = BASE_DIR / filepath
    if not full_path.exists():
        print(f"  SKIP: {filepath} (not found)")
        return

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changes += 1

    if content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [{label}] {filepath} - {changes} replacement(s)")
    else:
        print(f"  [{label}] {filepath} - no changes")


print("Updating remaining files...")
print("=" * 60)

# Doctor pages
doctor_files = [
    'doctors/prof-dr-md-golam-kabir.html',
    'doctors/dr-md-sahidur-rahman-milon.html',
    'doctors/dr-nh-tushar.html',
    'doctors/dr-shakila-zaman.html',
    'doctors/dr-md-dulal-hossain.html',
]

for f in doctor_files:
    update_file(f, DOCTOR_REPLACEMENTS, "DOCTOR")

# Admin login
update_file('admin/login.html', ADMIN_LOGIN_REPLACEMENTS, "ADMIN ")

# 404 - add a simple logo block
print("=" * 60)
print("Adding logo to 404 page...")
with open(BASE_DIR / '404.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the existing structure
new_404 = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex">
    <title>404 - Page Not Found | Green Hospital</title>
    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="images/favicon-16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&family=Noto+Sans+Bengali:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
    <style>
        body { display: flex; flex-direction: column; min-height: 100vh; }
        .error-container { flex: 1; display: flex; align-items: center; justify-content: center; padding: 2rem 1.5rem; }
    </style>
</head>
<body>
    <header style="padding: 1rem 1.5rem; border-bottom: 1px solid #e5e7eb;">
        <a href="/" style="display: inline-block;">
            <img src="images/logo.png" alt="Faridpur Green Hospital Ltd Official Logo" width="200" height="83" onerror="this.onerror=null; this.src='images/logo-official.jpg';">
        </a>
    </header>
    <div class="error-container">
        <div style="text-align: center;">
            <h1 style="font-size: 8rem; color: var(--clr-primary); margin: 0; line-height: 1;">404</h1>
            <h2 style="font-family: var(--font-heading); margin: 1rem 0; color: var(--clr-dark);">পেজটি পাওয়া যায়নি</h2>
            <p style="color: var(--clr-text-light); max-width: 500px; margin: 0 auto 2rem; line-height: 1.7;">
                দুঃখিত, আপনি যে পেজটি খুঁজছেন সেটি আমাদের সাইটে নেই। অনুগ্রহ করে অন্য কোনো লিংক ব্যবহার করুন।
            </p>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
                <a href="/" class="btn btn-primary">
                    <i class="fa-solid fa-house"></i> হোম পেজে যান
                </a>
                <a href="contact.html" class="btn btn-outline">
                    <i class="fa-solid fa-phone"></i> যোগাযোগ
                </a>
                <a href="tel:01988118833" class="btn btn-outline">
                    <i class="fa-solid fa-phone-volume"></i> 01988-118833
                </a>
            </div>
        </div>
    </div>
</body>
</html>'''

with open(BASE_DIR / '404.html', 'w', encoding='utf-8') as f:
    f.write(new_404)
print("  [404] 404.html - replaced with new content + logo")

print("=" * 60)
print("All done!")
