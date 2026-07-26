#!/usr/bin/env python3
"""
Generate individual doctor profile pages from data/doctors.json
This script creates a static HTML page for each doctor with full profile data.
"""
import json
import os
import sys
from pathlib import Path
import html

BASE_DIR = Path(r"D:\minimax\New folder\Green Hospital Ltd")
DOCTORS_DIR = BASE_DIR / "doctors"
DATA_FILE = BASE_DIR / "data" / "doctors.json"
HOSPITAL_FILE = BASE_DIR / "data" / "hospital.json"

# Read data
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    doctors_data = json.load(f)

with open(HOSPITAL_FILE, 'r', encoding='utf-8') as f:
    hospital = json.load(f)


def render(doctor, hospital):
    qualifications = ' · '.join(doctor['qualifications'])
    specialties_bn = ', '.join(doctor.get('specialties_bn', []))
    specialties_en = ', '.join(doctor.get('specialties_en', []))
    expertise = doctor.get('expertise', [])
    expertise_html = ''.join([f'<li><i class="fa-solid fa-check-circle"></i> {html.escape(e)}</li>' for e in expertise])
    qualifications_pills = ''.join([f'<span class="qualification-pill">{html.escape(q)}</span>' for q in doctor['qualifications']])
    specialty_pills = ''.join([f'<span class="specialty-pill"><i class="fa-solid fa-circle-check"></i> {html.escape(s)}</span>' for s in doctor.get('specialties_bn', [])])
    language_list = ''
    if doctor.get('languages'):
        language_list = ''.join([f'<li><i class="fa-solid fa-check"></i> {html.escape(lang)}</li>' for lang in doctor['languages']])

    image_src = doctor.get('image') or doctor.get('image_placeholder', '')
    onerror_js = doctor.get('image_placeholder', '').replace("'", "\\'")
    onerror_attr = f"this.onerror=null; this.src='{onerror_js}';"

    schedule_day = doctor['schedule'].get('day_en', '')
    schedule_time = doctor['schedule'].get('time_en', '')
    schedule_day_bn = doctor['schedule'].get('day_bn', '')
    schedule_time_bn = doctor['schedule'].get('time_bn', '')

    verified = bool(doctor.get('verified'))
    verified_badge_html = '<div class="verified-badge" title="Verified doctor"><i class="fa-solid fa-circle-check"></i> Verified</div>' if verified else ''

    experience_years = doctor.get('experience_years')
    experience_tag_html = f'<span class="experience-tag"><i class="fa-solid fa-award"></i> {experience_years}+ Years Experience</span>' if experience_years else ''

    expertise_section = ''
    if expertise:
        expertise_section = f'''<div class="detail-card">
                        <h2 class="detail-card-title"><i class="fa-solid fa-hand-holding-medical"></i> চিকিৎসা ও দক্ষতা</h2>
                        <ul class="expertise-list">
                            {expertise_html}
                        </ul>
                    </div>'''

    language_section = ''
    if language_list:
        language_section = f'''<div class="sidebar-card">
                        <h3><i class="fa-solid fa-language"></i> ভাষা</h3>
                        <ul class="language-list">
                            {language_list}
                        </ul>
                    </div>'''

    # Build JSON-LD structured data
    json_ld = {
        "@context": "https://schema.org",
        "@type": "Physician",
        "name": doctor['name_en'],
        "alternateName": doctor['name_bn'],
        "jobTitle": doctor['designation_en'],
        "affiliation": {
            "@type": "Hospital",
            "name": doctor.get('affiliation_en', hospital['name'])
        },
        "medicalSpecialty": doctor.get('specialties_en', []),
        "knowsLanguage": doctor.get('languages', []),
        "worksFor": {
            "@type": "Hospital",
            "name": hospital['name'],
            "address": hospital['address']['full'],
            "telephone": hospital['contact']['emergency']
        },
        "url": f"https://greenhospitalbd.com/doctors/{doctor['slug']}.html"
    }
    if experience_years:
        json_ld['experienceYears'] = experience_years
    json_ld_str = json.dumps(json_ld, ensure_ascii=False, indent=2)

    name_enc = html.escape(doctor['name_en'].replace(' ', '%20'))
    whatsapp_msg = f"স্যার/ম্যাডাম, আমি {doctor['name_en']}-এর চেম্বারে সিরিয়াল নিতে চাই।"
    whatsapp_msg_enc = html.escape(whatsapp_msg).replace(' ', '%20').replace('"', '%22').replace("'", "%27")
    
    # Build HTML
    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="bn">')
    parts.append('<head>')
    parts.append(f'    <meta charset="UTF-8">')
    parts.append(f'    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    specialty0 = doctor.get('specialties_en', ['Specialist'])[0] if doctor.get('specialties_en') else 'Specialist'
    parts.append(f'    <title>{html.escape(doctor["name_en"])} - {html.escape(specialty0)} | {html.escape(hospital["name"])}</title>')
    parts.append('')
    parts.append(f'    <meta name="description" content="{html.escape(doctor["name_en"])}, {html.escape(doctor["designation_en"])} at {html.escape(hospital["name"])}, Faridpur. {html.escape(qualifications)}. Chamber time: {html.escape(schedule_day)} {html.escape(schedule_time)}.">')
    parts.append(f'    <meta name="keywords" content="{html.escape(doctor["name_en"])}, {html.escape(specialty0)} Faridpur, Green Hospital Doctor, {html.escape(specialties_en)}">')
    parts.append(f'    <meta name="author" content="{html.escape(hospital["name"])}">')
    parts.append(f'    <link rel="canonical" href="https://greenhospitalbd.com/doctors/{doctor["slug"]}.html">')
    parts.append('')
    parts.append('    <!-- Open Graph -->')
    parts.append(f'    <meta property="og:title" content="{html.escape(doctor["name_en"])} - {html.escape(doctor["designation_en"])}">')
    parts.append(f'    <meta property="og:description" content="Chamber at {html.escape(hospital["name"])}: {html.escape(schedule_day)} {html.escape(schedule_time)}. {html.escape(qualifications)}.">')
    parts.append(f'    <meta property="og:image" content="https://greenhospitalbd.com/{image_src}">')
    parts.append(f'    <meta property="og:url" content="https://greenhospitalbd.com/doctors/{doctor["slug"]}.html">')
    parts.append(f'    <meta property="og:type" content="profile">')
    parts.append('')
    parts.append('    <!-- Twitter Card -->')
    parts.append('    <meta name="twitter:card" content="summary_large_image">')
    parts.append(f'    <meta name="twitter:title" content="{html.escape(doctor["name_en"])} - {html.escape(hospital["name"])}">')
    parts.append(f'    <meta name="twitter:description" content="{html.escape(doctor["designation_en"])}. {html.escape(schedule_day)} {html.escape(schedule_time)}.">')
    parts.append('')
    parts.append('    <!-- JSON-LD Structured Data -->')
    parts.append('    <script type="application/ld+json">')
    parts.append(json_ld_str)
    parts.append('    </script>')
    parts.append('')
    parts.append('    <!-- Preconnect -->')
    parts.append('    <link rel="preconnect" href="https://fonts.googleapis.com">')
    parts.append('    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    parts.append('    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>')
    parts.append('')
    parts.append('    <!-- Google Fonts -->')
    parts.append('    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&family=Noto+Sans+Bengali:wght@400;500;600;700&display=swap" rel="stylesheet">')
    parts.append('')
    parts.append('    <!-- Font Awesome -->')
    parts.append('    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">')
    parts.append('')
    parts.append('    <!-- Main CSS -->')
    parts.append('    <link rel="stylesheet" href="../styles.css">')
    parts.append('    <link rel="stylesheet" href="doctor-profile.css">')
    parts.append('')
    parts.append('    <!-- PWA -->')
    parts.append('    <link rel="manifest" href="../manifest.json">')
    parts.append('    <meta name="theme-color" content="#0a8d4a">')
    parts.append('</head>')
    parts.append('<body>')
    # Top Bar
    parts.append('    <!-- Top Bar -->')
    parts.append('    <div class="top-bar">')
    parts.append('        <div class="container">')
    parts.append('            <div class="top-bar-content">')
    parts.append('                <div class="emergency-contact">')
    parts.append('                    <i class="fa-solid fa-phone-volume fa-shake"></i>')
    parts.append(f'                    <span>২৪/৭ জরুরি সেবা: <a href="tel:{hospital["contact"]["emergency"]}">{html.escape(hospital["contact"]["emergency_formatted"])}</a></span>')
    parts.append('                </div>')
    parts.append('                <div class="top-social">')
    parts.append(f'                    <a href="{hospital["social"]["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>')
    parts.append(f'                    <a href="mailto:{hospital["contact"]["email"]}" aria-label="Email"><i class="fa-solid fa-envelope"></i></a>')
    parts.append('                </div>')
    parts.append('            </div>')
    parts.append('        </div>')
    parts.append('    </div>')
    parts.append('')
    # Navigation
    parts.append('    <!-- Navigation -->')
    parts.append('    <header class="header">')
    parts.append('        <div class="container">')
    parts.append('            <nav class="navbar">')
    parts.append('                <div class="logo">')
    parts.append('                    <a href="../index.html">')
    parts.append(f'                        <img src="../images/logo.jpg" alt="{html.escape(hospital["name"])} Logo" onerror="this.onerror=null; this.src=\'https://placehold.co/200x60?text=Green+Hospital\';">')
    parts.append('                        <span class="logo-text">গ্রিন হাসপাতাল</span>')
    parts.append('                    </a>')
    parts.append('                </div>')
    parts.append('                <div class="mobile-menu-btn" aria-label="Toggle menu">')
    parts.append('                    <i class="fa-solid fa-bars"></i>')
    parts.append('                </div>')
    parts.append('                <ul class="nav-links">')
    parts.append('                    <li><a href="../index.html">হোম</a></li>')
    parts.append('                    <li><a href="../about.html">আমাদের সম্পর্কে</a></li>')
    parts.append('                    <li><a href="../services.html">সেবা সমূহ</a></li>')
    parts.append('                    <li><a href="../doctors.html" class="active">ডাক্তার তালিকা</a></li>')
    parts.append('                    <li><a href="../contact.html">যোগাযোগ</a></li>')
    parts.append('                </ul>')
    parts.append('                <div class="nav-btn">')
    parts.append('                    <a href="../contact.html#appointment" class="btn btn-primary">অ্যাপয়েন্টমেন্ট নিন</a>')
    parts.append('                </div>')
    parts.append('            </nav>')
    parts.append('        </div>')
    parts.append('    </header>')
    parts.append('')
    # Profile Hero
    parts.append('    <!-- Doctor Profile Hero -->')
    parts.append('    <section class="doctor-profile-hero">')
    parts.append('        <div class="container">')
    parts.append('            <div class="doctor-profile-grid">')
    parts.append('                <!-- Image -->')
    parts.append('                <div class="doctor-profile-image">')
    parts.append('                    <div class="doctor-image-wrapper">')
    parts.append(f'                        <img src="../{image_src}" alt="{html.escape(doctor["name_en"])}" onerror="{onerror_attr}">')
    parts.append(f'                        {verified_badge_html}')
    parts.append('                    </div>')
    parts.append('                </div>')
    parts.append('                <!-- Info -->')
    parts.append('                <div class="doctor-profile-info">')
    parts.append('                    <div class="doctor-profile-meta">')
    parts.append(f'                        <span class="specialty-tag"><i class="fa-solid fa-stethoscope"></i> {html.escape(doctor["department_bn"])}</span>')
    parts.append(f'                        {experience_tag_html}')
    parts.append('                    </div>')
    parts.append(f'                    <h1 class="doctor-profile-name">{html.escape(doctor["name_bn"])}</h1>')
    parts.append(f'                    <h2 class="doctor-profile-name-en">{html.escape(doctor["name_en"])}</h2>')
    parts.append(f'                    <p class="doctor-designation"><i class="fa-solid fa-user-md"></i> {html.escape(doctor["designation_bn"])}</p>')
    parts.append(f'                    <p class="doctor-affiliation"><i class="fa-solid fa-hospital"></i> {html.escape(doctor["affiliation_bn"])}</p>')
    parts.append('                    <div class="doctor-qualifications">')
    parts.append('                        <h3><i class="fa-solid fa-graduation-cap"></i> শিক্ষাগত যোগ্যতা</h3>')
    parts.append('                        <div class="qualifications-list">')
    parts.append(f'                            {qualifications_pills}')
    parts.append('                        </div>')
    parts.append('                    </div>')
    parts.append('                    <div class="quick-schedule-card">')
    parts.append('                        <div class="schedule-header">')
    parts.append('                            <i class="fa-regular fa-calendar-check"></i>')
    parts.append('                            <span>চেম্বারের সময়সূচি</span>')
    parts.append('                        </div>')
    parts.append(f'                        <div class="schedule-day">{html.escape(schedule_day_bn)}</div>')
    parts.append(f'                        <div class="schedule-time">{html.escape(schedule_time_bn)}</div>')
    parts.append('                    </div>')
    parts.append('                    <div class="doctor-cta-buttons">')
    parts.append(f'                        <a href="tel:{hospital["contact"]["emergency"]}" class="btn btn-primary btn-lg">')
    parts.append(f'                            <i class="fa-solid fa-phone-volume"></i> সিরিয়াল নিন: {html.escape(hospital["contact"]["emergency_formatted"])}')
    parts.append('                        </a>')
    parts.append(f'                        <a href="https://wa.me/8801988118833?text={whatsapp_msg_enc}" class="btn btn-outline btn-lg" target="_blank" rel="noopener">')
    parts.append('                            <i class="fa-brands fa-whatsapp"></i> WhatsApp')
    parts.append('                        </a>')
    parts.append('                    </div>')
    parts.append('                </div>')
    parts.append('            </div>')
    parts.append('        </div>')
    parts.append('    </section>')
    parts.append('')
    # Details
    parts.append('    <!-- Detailed Sections -->')
    parts.append('    <section class="doctor-details-section">')
    parts.append('        <div class="container">')
    parts.append('            <div class="doctor-details-grid">')
    parts.append('                <div class="doctor-main-content">')
    parts.append('                    <div class="detail-card">')
    parts.append('                        <h2 class="detail-card-title"><i class="fa-solid fa-user-md"></i> ডাক্তার সম্পর্কে</h2>')
    parts.append(f'                        <p class="doctor-bio">{html.escape(doctor.get("bio_bn", ""))}</p>')
    parts.append('                    </div>')
    parts.append('                    <div class="detail-card">')
    parts.append('                        <h2 class="detail-card-title"><i class="fa-solid fa-microscope"></i> বিশেষজ্ঞতা</h2>')
    parts.append('                        <div class="specialties-tags">')
    parts.append(f'                            {specialty_pills}')
    parts.append('                        </div>')
    parts.append('                    </div>')
    parts.append(f'                    {expertise_section}')
    parts.append('                    <div class="detail-card schedule-card">')
    parts.append('                        <h2 class="detail-card-title"><i class="fa-regular fa-clock"></i> চেম্বারের বিস্তারিত সময়সূচি</h2>')
    parts.append('                        <div class="schedule-grid">')
    parts.append('                            <div class="schedule-item">')
    parts.append('                                <i class="fa-regular fa-calendar"></i>')
    parts.append('                                <div>')
    parts.append('                                    <strong>চেম্বারের দিন</strong>')
    parts.append(f'                                    <p>{html.escape(schedule_day_bn)} ({html.escape(schedule_day)})</p>')
    parts.append('                                </div>')
    parts.append('                            </div>')
    parts.append('                            <div class="schedule-item">')
    parts.append('                                <i class="fa-regular fa-clock"></i>')
    parts.append('                                <div>')
    parts.append('                                    <strong>চেম্বারের সময়</strong>')
    parts.append(f'                                    <p>{html.escape(schedule_time_bn)} ({html.escape(schedule_time)})</p>')
    parts.append('                                </div>')
    parts.append('                            </div>')
    parts.append('                            <div class="schedule-item">')
    parts.append('                                <i class="fa-solid fa-money-bill"></i>')
    parts.append('                                <div>')
    parts.append('                                    <strong>পরামর্শ ফি</strong>')
    parts.append(f'                                    <p>{html.escape(doctor.get("consultation_fee", "ফোনে জানতে কল করুন"))}</p>')
    parts.append('                                </div>')
    parts.append('                            </div>')
    parts.append('                            <div class="schedule-item">')
    parts.append('                                <i class="fa-solid fa-phone"></i>')
    parts.append('                                <div>')
    parts.append('                                    <strong>সিরিয়াল নম্বর</strong>')
    parts.append(f'                                    <p><a href="tel:{hospital["contact"]["emergency"]}">{html.escape(hospital["contact"]["emergency_formatted"])}</a></p>')
    parts.append('                                </div>')
    parts.append('                            </div>')
    parts.append('                        </div>')
    parts.append('                        <div class="schedule-note">')
    parts.append('                            <i class="fa-solid fa-circle-info"></i>')
    parts.append('                            <span>সময়সূচি পরিবর্তন হতে পারে। আসার পূর্বে কল করে নিশ্চিত হোন।</span>')
    parts.append('                        </div>')
    parts.append('                    </div>')
    parts.append('                </div>')
    parts.append('')
    # Sidebar
    parts.append('                <aside class="doctor-sidebar">')
    parts.append('                    <div class="sidebar-card appointment-card">')
    parts.append('                        <h3><i class="fa-solid fa-calendar-plus"></i> অ্যাপয়েন্টমেন্ট নিন</h3>')
    parts.append('                        <p>এই ডাক্তারের চেম্বারে সিরিয়াল বুক করতে এখনই কল করুন অথবা WhatsApp-এ মেসেজ করুন।</p>')
    parts.append(f'                        <a href="tel:{hospital["contact"]["emergency"]}" class="btn btn-primary btn-block">')
    parts.append(f'                            <i class="fa-solid fa-phone"></i> {html.escape(hospital["contact"]["emergency_formatted"])}')
    parts.append('                        </a>')
    parts.append(f'                        <a href="https://wa.me/8801988118833?text={whatsapp_msg_enc}" class="btn btn-whatsapp btn-block" target="_blank" rel="noopener">')
    parts.append('                            <i class="fa-brands fa-whatsapp"></i> WhatsApp-এ মেসেজ')
    parts.append('                        </a>')
    parts.append('                        <a href="../contact.html#appointment" class="btn btn-outline btn-block">')
    parts.append('                            <i class="fa-solid fa-envelope"></i> অনলাইন বার্তা')
    parts.append('                        </a>')
    parts.append('                    </div>')
    parts.append(f'                    {language_section}')
    parts.append('                    <div class="sidebar-card">')
    parts.append('                        <h3><i class="fa-solid fa-hospital"></i> হাসপাতালের তথ্য</h3>')
    parts.append('                        <ul class="hospital-info-list">')
    parts.append(f'                            <li><i class="fa-solid fa-location-dot"></i> <span>{html.escape(hospital["address"]["full"])}</span></li>')
    parts.append(f'                            <li><i class="fa-solid fa-phone"></i> <a href="tel:{hospital["contact"]["emergency"]}">{html.escape(hospital["contact"]["emergency_formatted"])}</a></li>')
    parts.append(f'                            <li><i class="fa-solid fa-envelope"></i> <a href="mailto:{hospital["contact"]["email"]}">{html.escape(hospital["contact"]["email"])}</a></li>')
    parts.append('                        </ul>')
    parts.append('                    </div>')
    parts.append('                    <div class="sidebar-card">')
    parts.append('                        <h3><i class="fa-solid fa-share-nodes"></i> শেয়ার করুন</h3>')
    parts.append('                        <div class="share-buttons">')
    parts.append(f'                            <a href="https://www.facebook.com/sharer/sharer.php?u=https://greenhospitalbd.com/doctors/{doctor["slug"]}.html" target="_blank" rel="noopener" class="share-btn facebook" aria-label="Share on Facebook"><i class="fa-brands fa-facebook-f"></i></a>')
    parts.append(f'                            <a href="https://wa.me/?text={html.escape(doctor["name_en"])}%20-%20{html.escape(hospital["name"])}%20https%3A%2F%2Fgreenhospitalbd.com%2Fdoctors%2F{doctor["slug"]}.html" target="_blank" rel="noopener" class="share-btn whatsapp" aria-label="Share on WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>')
    parts.append('                            <button class="share-btn copy-link" onclick="copyDoctorLink()" aria-label="Copy link"><i class="fa-solid fa-link"></i></button>')
    parts.append('                        </div>')
    parts.append('                    </div>')
    parts.append('                </aside>')
    parts.append('            </div>')
    parts.append('        </div>')
    parts.append('    </section>')
    parts.append('')
    # Other doctors
    parts.append('    <section class="other-doctors-section">')
    parts.append('        <div class="container">')
    parts.append('            <div class="section-header text-center">')
    parts.append('                <h2>আমাদের অন্যান্য বিশেষজ্ঞ ডাক্তারগণ</h2>')
    parts.append('                <p>ফরিদপুর গ্রিন হাসপাতালের অভিজ্ঞ চিকিৎসকদের প্যানেল</p>')
    parts.append('            </div>')
    parts.append('            <div class="other-doctors-grid" id="otherDoctorsGrid"></div>')
    parts.append('            <div class="text-center mt-4">')
    parts.append('                <a href="../doctors.html" class="btn btn-primary">সকল ডাক্তার দেখুন <i class="fa-solid fa-arrow-right"></i></a>')
    parts.append('            </div>')
    parts.append('        </div>')
    parts.append('    </section>')
    parts.append('')
    # Footer
    parts.append('    <footer class="footer">')
    parts.append('        <div class="footer-top">')
    parts.append('            <div class="container">')
    parts.append('                <div class="footer-grid">')
    parts.append('                    <div class="footer-widget info-widget">')
    parts.append('                        <img src="../images/logo.jpg" alt="Logo" class="footer-logo" onerror="this.onerror=null; this.src=\'https://placehold.co/200x60?text=Logo\';">')
    parts.append(f'                        <p class="footer-desc">{html.escape(hospital["name"])} - আধুনিক চিকিৎসা বিজ্ঞান এবং মানবিক সেবার এক অনন্য মেলবন্ধন।</p>')
    parts.append('                        <div class="footer-social">')
    parts.append(f'                            <a href="{hospital["social"]["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>')
    parts.append(f'                            <a href="mailto:{hospital["contact"]["email"]}" aria-label="Email"><i class="fa-solid fa-envelope"></i></a>')
    parts.append('                            <a href="https://wa.me/8801988118833" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>')
    parts.append('                        </div>')
    parts.append('                    </div>')
    parts.append('                    <div class="footer-widget links-widget">')
    parts.append('                        <h3>প্রয়োজনীয় লিংক</h3>')
    parts.append('                        <ul>')
    parts.append('                            <li><a href="../index.html">হোম</a></li>')
    parts.append('                            <li><a href="../about.html">আমাদের সম্পর্কে</a></li>')
    parts.append('                            <li><a href="../services.html">সেবা সমূহ</a></li>')
    parts.append('                            <li><a href="../doctors.html">ডাক্তার তালিকা</a></li>')
    parts.append('                            <li><a href="../contact.html">যোগাযোগ</a></li>')
    parts.append('                        </ul>')
    parts.append('                    </div>')
    parts.append('                    <div class="footer-widget contact-widget">')
    parts.append('                        <h3>যোগাযোগের ঠিকানা</h3>')
    parts.append('                        <ul class="contact-list">')
    parts.append(f'                            <li><i class="fa-solid fa-location-dot"></i> <span>{html.escape(hospital["address"]["full"])}</span></li>')
    parts.append(f'                            <li><i class="fa-solid fa-phone"></i> <span><a href="tel:{hospital["contact"]["emergency"]}">{html.escape(hospital["contact"]["emergency_formatted"])}</a></span></li>')
    parts.append(f'                            <li><i class="fa-solid fa-envelope"></i> <span><a href="mailto:{hospital["contact"]["email"]}">{html.escape(hospital["contact"]["email"])}</a></span></li>')
    parts.append('                        </ul>')
    parts.append('                    </div>')
    parts.append('                    <div class="footer-widget map-widget">')
    parts.append('                        <h3>লোকেশন ম্যাপ</h3>')
    parts.append('                        <div class="map-container">')
    parts.append('                            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d117070.78160451006!2d89.74900762190807!3d23.601732559599554!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39fe07f0f70e7e1f%3A0x892a0129c540daeb!2sGreen%20Hospital%20%26%20Diagnostic%20Center!5e0!3m2!1sen!2sbd!4v1689240409867!5m2!1sen!2sbd" width="100%" height="150" style="border:0; border-radius: 5px;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')
    parts.append('                        </div>')
    parts.append('                    </div>')
    parts.append('                </div>')
    parts.append('            </div>')
    parts.append('        </div>')
    parts.append('        <div class="footer-bottom">')
    parts.append('            <div class="container">')
    parts.append('                <div class="copyright-text">')
    parts.append('                    <p>&copy; <span id="currentYear"></span> গ্রিন হাসপাতাল লিমিটেড. সর্বস্বত্ব সংরক্ষিত।</p>')
    parts.append('                </div>')
    parts.append('            </div>')
    parts.append('        </div>')
    parts.append('    </footer>')
    parts.append('')
    # Floating buttons
    parts.append(f'    <a href="https://wa.me/8801988118833?text={whatsapp_msg_enc}" class="whatsapp-float" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">')
    parts.append('        <i class="fa-brands fa-whatsapp"></i>')
    parts.append('    </a>')
    parts.append('    <button id="scrollToTop" class="scroll-to-top" aria-label="Scroll to top">')
    parts.append('        <i class="fa-solid fa-arrow-up"></i>')
    parts.append('    </button>')
    parts.append('')
    # Script
    parts.append('    <script>')
    parts.append('        document.getElementById(\'currentYear\').textContent = new Date().getFullYear();')
    parts.append('        function copyDoctorLink() {')
    parts.append('            const url = window.location.href;')
    parts.append('            navigator.clipboard.writeText(url).then(() => {')
    parts.append('                const btn = document.querySelector(\'.copy-link\');')
    parts.append('                const orig = btn.innerHTML;')
    parts.append('                btn.innerHTML = \'<i class="fa-solid fa-check"></i>\';')
    parts.append('                setTimeout(() => { btn.innerHTML = orig; }, 2000);')
    parts.append('            });')
    parts.append('        }')
    parts.append(f'        const currentDoctor = \'{doctor["id"]}\';')
    parts.append('        fetch(\'../data/doctors.json\')')
    parts.append('            .then(r => r.json())')
    parts.append('            .then(data => {')
    parts.append('                const grid = document.getElementById(\'otherDoctorsGrid\');')
    parts.append('                const others = data.doctors.filter(d => d.id !== currentDoctor).slice(0, 4);')
    parts.append('                grid.innerHTML = others.map(d => \`')
    parts.append('                    <a href="\${d.slug}.html" class="other-doctor-card">')
    parts.append('                        <div class="other-doctor-img">')
    parts.append('                            <img src="../\${d.image}" alt="\${d.name_en}" onerror="this.onerror=null; this.src=\'\${d.image_placeholder}\';">')
    parts.append('                        </div>')
    parts.append('                        <div class="other-doctor-info">')
    parts.append('                            <h4>\${d.name_bn}</h4>')
    parts.append('                            <p class="other-deg">\${d.qualifications.slice(0, 2).join(\', \')}\${d.qualifications.length > 2 ? \'...\' : \'\'}</p>')
    parts.append('                            <p class="other-spec">\${d.specialties_bn[0] || \'\'}</p>')
    parts.append('                        </div>')
    parts.append('                    </a>')
    parts.append('                \`).join(\'\');')
    parts.append('            })')
    parts.append('            .catch(err => console.error(\'Error loading doctors:\', err));')
    parts.append('    </script>')
    parts.append('    <script src="../script.js"></script>')
    parts.append('</body>')
    parts.append('</html>')
    return '\n'.join(parts)


DOCTORS_DIR.mkdir(parents=True, exist_ok=True)

for doctor in doctors_data['doctors']:
    page_html = render(doctor, hospital)
    output_path = DOCTORS_DIR / f"{doctor['slug']}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"OK Generated: {output_path.name}")

print(f"\nAll {len(doctors_data['doctors'])} doctor profile pages generated in {DOCTORS_DIR}")
