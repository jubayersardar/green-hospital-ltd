# Faridpur Green Hospital Ltd - Official Website

> Production-ready enterprise-grade hospital website built for **Faridpur Green Hospital Ltd**, Bangladesh.

![Status](https://img.shields.io/badge/status-production--ready-success)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-proprietary-red)

## 🏥 Overview

A complete, modern, mobile-first website for Faridpur Green Hospital Ltd featuring:

- **5 main pages** + 5 individual doctor profile pages
- **PHP backend** for contact forms & appointments
- **Admin panel** for managing submissions
- **PWA** (Progressive Web App) support with offline capability
- **Schema.org** structured data for SEO
- **Bangla-first** bilingual content (Bangla primary, English secondary)
- **Accessibility** WCAG 2.1 AA compliant

## 📁 Project Structure

```
Green Hospital Ltd/
├── index.html              # Homepage
├── about.html              # About Us
├── services.html           # All Services
├── doctors.html            # Doctors List (with search & filter)
├── contact.html            # Contact + Appointment Form
├── 404.html                # Custom 404 page
│
├── styles.css              # Production stylesheet (29KB)
├── script.js               # Interactive features (14KB)
│
├── manifest.json           # PWA manifest
├── service-worker.js       # PWA offline support
├── robots.txt              # SEO robots
├── sitemap.xml             # XML sitemap
├── .htaccess               # Apache config (security + perf)
│
├── data/                   # Data files
│   ├── hospital.json       # Hospital info
│   ├── doctors.json        # 5 verified doctors
│   ├── services.json       # 13 services + 6 facilities
│   └── submissions/        # Form submissions (auto-created)
│
├── doctors/                # Individual doctor pages
│   ├── prof-dr-md-golam-kabir.html
│   ├── dr-md-sahidur-rahman-milon.html
│   ├── dr-nh-tushar.html
│   ├── dr-shakila-zaman.html
│   ├── dr-md-dulal-hossain.html
│   ├── doctor-profile.css
│   └── images/             # Doctor portrait images
│
├── images/                 # Hospital images
│   ├── logo.jpg
│   ├── hospital-hero.jpg
│   ├── about-hospital.jpg
│   ├── medical-team.jpg
│   ├── diagnostic-lab.jpg
│   ├── operation-theater.jpg
│   └── emergency-service.jpg
│
├── api/                    # PHP Backend API
│   ├── config.php          # Configuration
│   ├── contact.php         # Contact form handler
│   └── appointment.php     # Appointment booking handler
│
├── admin/                  # Admin Panel
│   ├── login.html          # Admin login page
│   ├── auth.php            # Authentication
│   ├── dashboard.php       # Submissions dashboard
│   └── logout.php          # Logout
│
└── tools/                  # Build tools
    └── generate_doctor_pages.py
```

## 🚀 Quick Start

### Requirements
- PHP 7.4+ (with `mail()` function enabled)
- Apache with `mod_rewrite`, `mod_headers`, `mod_deflate`, `mod_expires`
- Modern web browser
- For dev: Python 3 (for regen scripts)

### Installation
1. Upload all files to web root (e.g., `/var/www/html/` or `htdocs/`)
2. Ensure `data/submissions/` is writable: `chmod 755 data/`
3. Configure email in `api/config.php`
4. **Change admin password** in `api/config.php` (default: `GreenHospital2026!`)
5. Enable HTTPS for production
6. Update site URL in:
   - `robots.txt`
   - `sitemap.xml`
   - `script.js` (service worker)
   - `manifest.json`

### Default Admin Credentials
- **URL**: `/admin/login.html`
- **Username**: `admin`
- **Password**: `GreenHospital2026!` ← **CHANGE THIS IMMEDIATELY!**

## 🔧 Configuration

Edit `api/config.php`:

```php
define('HOSPITAL_PHONE', '+8801988118833');
define('HOSPITAL_EMAIL', 'info@greenhospitalbd.com');
define('NOTIFICATION_EMAIL', 'info@greenhospitalbd.com');
define('ADMIN_USERNAME', 'admin');
define('ADMIN_PASSWORD_HASH', '$2y$10$...'); // Generate new hash
```

### Generate New Admin Password Hash
```php
echo password_hash('YourNewPassword', PASSWORD_DEFAULT);
```

## 📋 Data Management

### Adding a New Doctor
1. Add doctor to `data/doctors.json`:
```json
{
  "id": "unique-slug",
  "name_bn": "ডা. ...",
  "name_en": "Dr. ...",
  "title": "Doctor",
  "designation_bn": "...",
  "designation_en": "...",
  "affiliation_bn": "...",
  "affiliation_en": "...",
  "qualifications": ["MBBS", "FCPS"],
  "specialties_bn": ["..."],
  "specialties_en": ["..."],
  "expertise": ["..."],
  "department": "orthopedics",
  "department_bn": "অর্থোপেডিকস",
  "experience_years": 10,
  "languages": ["Bangla", "English"],
  "schedule": {
    "day_en": "Every Friday",
    "day_bn": "প্রতি শুক্রবার",
    "time_en": "9:00 AM - 5:00 PM",
    "time_bn": "সকাল ৯:০০ - বিকাল ৫:০০"
  },
  "serial_number": "01988-118833",
  "consultation_fee": "৫০০ টাকা",
  "image": "images/doctors/photo.jpg",
  "image_placeholder": "https://placehold.co/600x600/0a8d4a/ffffff?text=Dr.+Name",
  "verified": true,
  "source": "Manual entry",
  "bio_bn": "...",
  "bio_en": "..."
}
```
2. Run `python tools/generate_doctor_pages.py` to create the page
3. Add doctor photo to `doctors/images/`

### Adding a New Service
Edit `data/services.json` and add a new service object.

## 🎨 Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --clr-primary: #0a8d4a;       /* Main brand color */
    --clr-primary-dark: #076835;
    --clr-accent: #ffc107;        /* Highlight color */
    /* ... */
}
```

### Contact Info
Update everywhere via:
- `data/hospital.json`
- Footer in each HTML file
- Schema.org JSON-LD

## 🔒 Security Features

- ✅ HTTPS forced (HSTS enabled)
- ✅ Security headers (CSP, X-Frame-Options, X-XSS-Protection, etc.)
- ✅ Rate limiting on forms
- ✅ Honeypot anti-spam
- ✅ Input validation & sanitization
- ✅ SQL injection-safe (no SQL used)
- ✅ XSS protection
- ✅ CSRF protection on forms
- ✅ Session management for admin
- ✅ Password hashing (bcrypt)
- ✅ File access protection (.htaccess)

## 🚀 Performance

- ✅ Gzip compression
- ✅ Browser caching (1 year for images, 1 month for CSS/JS)
- ✅ Preconnect to CDNs
- ✅ Lazy loading images
- ✅ Service worker offline support
- ✅ Minified-ready CSS
- ✅ DNS prefetching

## 📊 SEO Features

- ✅ Schema.org structured data (Hospital, Physician, Service, LocalBusiness)
- ✅ Open Graph tags
- ✅ Twitter Card
- ✅ XML Sitemap
- ✅ robots.txt
- ✅ Canonical URLs
- ✅ Meta descriptions & keywords
- ✅ Bangla + English bilingual
- ✅ Geo metadata
- ✅ Semantic HTML5

## 🧪 Testing Checklist

Before going live, verify:

- [ ] All pages load (5 main + 5 doctor pages)
- [ ] Mobile responsive on all devices
- [ ] Contact form submits successfully
- [ ] Appointment form submits successfully
- [ ] Email notifications arrive
- [ ] Admin login works
- [ ] Admin dashboard shows submissions
- [ ] All phone numbers clickable (`tel:`)
- [ ] WhatsApp links work
- [ ] Google Maps embed loads
- [ ] All images load (no 404s)
- [ ] Service Worker registers
- [ ] SSL certificate active
- [ ] Sitemap accessible
- [ ] robots.txt accessible
- [ ] Schema.org validates (https://validator.schema.org/)

## 🐛 Troubleshooting

### Forms not sending emails
1. Check PHP `mail()` is configured: `<?php phpinfo(); ?>`
2. Check `data/submissions/` is writable
3. Use SMTP plugin like PHPMailer for better email delivery

### Service Worker not registering
- SW only registers on HTTPS (or localhost)
- Check browser console for errors

### Admin login failing
- Verify password hash in `api/config.php` matches password
- Clear browser cookies and try again

## 📞 Support

- **Hospital**: 01988-118833
- **Email**: info@greenhospitalbd.com
- **Address**: Kabi Jasim Uddin Road, Alipur, Faridpur Sadar, Faridpur

## 📄 License

Proprietary © 2026 Faridpur Green Hospital Ltd. All rights reserved.

---

**Built with ❤️ for better healthcare in Faridpur**
