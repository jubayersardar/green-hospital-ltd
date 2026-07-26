#!/usr/bin/env python3
"""
Embed doctor data directly into HTML pages as JSON script tags.
This makes the pages work even if fetch fails (CORS, server down, etc.)
"""
import json
import re
from pathlib import Path

BASE_DIR = Path(r"D:\minimax\New folder\Green Hospital Ltd")

# Read doctors.json
with open(BASE_DIR / "data" / "doctors.json", "r", encoding="utf-8") as f:
    doctors_data = json.load(f)

doctors_json = json.dumps(doctors_data, ensure_ascii=False)

# Read services.json
with open(BASE_DIR / "data" / "services.json", "r", encoding="utf-8") as f:
    services_data = json.load(f)

services_json = json.dumps(services_data, ensure_ascii=False)


def embed_data_in_html(html_path, doctors_json, services_json=None):
    """Embed data as script tags in the HTML file"""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build the embedded data script
    embedded_scripts = f'''<!-- Embedded data for offline/robust loading -->
    <script type="application/json" id="doctors-data">
{doctors_json}
    </script>
'''

    if services_json:
        embedded_scripts += f'''    <script type="application/json" id="services-data">
{services_json}
    </script>
'''

    # Insert before </head>
    if "</head>" in content:
        # Check if already embedded
        if 'id="doctors-data"' in content:
            # Replace existing
            content = re.sub(
                r'<script type="application/json" id="doctors-data">.*?</script>\s*<script type="application/json" id="services-data">.*?</script>',
                embedded_scripts.strip(),
                content,
                flags=re.DOTALL
            )
            # Or replace just doctors-data
            content = re.sub(
                r'<script type="application/json" id="doctors-data">.*?</script>',
                f'<script type="application/json" id="doctors-data">\n{doctors_json}\n    </script>',
                content,
                flags=re.DOTALL
            )
        else:
            content = content.replace("</head>", embedded_scripts + "\n</head>")

    # Now update the JavaScript to use the embedded data first
    # Replace the fetch logic with a function that tries embedded data first, then fetch
    return content


# Pages to update
pages = ["index.html", "doctors.html", "services.html", "about.html", "contact.html"]

for page in pages:
    page_path = BASE_DIR / page
    if page_path.exists():
        new_content = embed_data_in_html(str(page_path), doctors_json, services_json)
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"OK Updated: {page}")
    else:
        print(f"SKIP: {page} (not found)")


# Now update the JavaScript in each file to use embedded data with fallback
print("\nNow updating JavaScript logic...")

# Update index.html
with open(BASE_DIR / "index.html", "r", encoding="utf-8") as f:
    content = f.read()

new_index_js = '''    <script>
        // Set current year
        document.getElementById('currentYear').textContent = new Date().getFullYear();
        
        // Load services with embedded data + fetch fallback
        function loadServices() {
            const grid = document.getElementById('servicesGrid');
            let data = null;
            
            // Try embedded data first
            const embedded = document.getElementById('services-data');
            if (embedded) {
                try { data = JSON.parse(embedded.textContent); } catch(e) {}
            }
            
            // Try fetch as update
            fetch('data/services.json')
                .then(r => r.json())
                .then(fetched => renderServices(fetched))
                .catch(() => { if (data) renderServices(data); else grid.innerHTML = '<p style="text-align:center;color:#999;padding:2rem;">Services data unavailable</p>'; });
            
            function renderServices(d) {
                if (!d || !d.services) return;
                grid.innerHTML = d.services.slice(0, 6).map(s => `
                    <div class="service-card">
                        <i class="fa-solid ${s.icon}"></i>
                        <h3 class="service-title">${s.name_bn}</h3>
                        <p>${s.description_bn}</p>
                    </div>
                `).join('');
            }
            
            if (data) renderServices(data);
        }
        
        // Load doctors with embedded data + fetch fallback
        function loadDoctors() {
            const grid = document.getElementById('doctorsGrid');
            let data = null;
            
            const embedded = document.getElementById('doctors-data');
            if (embedded) {
                try { data = JSON.parse(embedded.textContent); } catch(e) {}
            }
            
            fetch('data/doctors.json')
                .then(r => r.json())
                .then(fetched => renderDoctors(fetched))
                .catch(() => { if (data) renderDoctors(data); else grid.innerHTML = '<p style="text-align:center;color:#999;padding:2rem;">Doctor data unavailable</p>'; });
            
            function renderDoctors(d) {
                if (!d || !d.doctors) return;
                grid.innerHTML = d.doctors.map(doc => `
                    <article class="doctor-card" itemscope itemtype="https://schema.org/Physician">
                        <meta itemprop="medicalSpecialty" content="${(doc.specialties_en || []).join(', ')}">
                        <div class="doctor-avatar">
                            <img src="${doc.image}" alt="${doc.name_en}" itemprop="image" loading="lazy" onerror="this.onerror=null; this.src='${doc.image_placeholder}';">
                        </div>
                        <h3 itemprop="name">${doc.name_bn}</h3>
                        <span class="specialty" itemprop="jobTitle">${doc.specialties_bn[0] || doc.department_bn}</span>
                        <p class="degrees">${doc.qualifications.slice(0, 2).join(', ')}</p>
                        <div class="schedule">
                            <i class="fa-regular fa-clock"></i>
                            <span>${doc.schedule.day_bn} ${doc.schedule.time_bn}</span>
                        </div>
                        <a href="doctors/${doc.slug}.html" class="btn btn-primary">
                            <i class="fa-solid fa-user-doctor"></i> প্রোফাইল দেখুন
                        </a>
                    </article>
                `).join('');
            }
            
            if (data) renderDoctors(data);
        }
        
        loadServices();
        loadDoctors();
    </script>'''

# Replace the old script block
content = re.sub(
    r'<script>\s*// Set current year.*?</script>',
    new_index_js,
    content,
    flags=re.DOTALL
)
with open(BASE_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK Updated index.html JS")

# Update doctors.html
with open(BASE_DIR / "doctors.html", "r", encoding="utf-8") as f:
    content = f.read()

new_doctors_js = '''    <script>
        document.getElementById('currentYear').textContent = new Date().getFullYear();
        
        // Load doctors with embedded data + fetch fallback
        let allDoctors = [];
        
        (function loadDoctorData() {
            const grid = document.getElementById('doctorsList');
            let data = null;
            
            // Try embedded data first
            const embedded = document.getElementById('doctors-data');
            if (embedded) {
                try { data = JSON.parse(embedded.textContent); } catch(e) { console.error('Embedded parse failed:', e); }
            }
            
            // Try fetch as fresh data
            fetch('data/doctors.json')
                .then(r => r.json())
                .then(fetched => {
                    allDoctors = fetched.doctors;
                    renderDoctors(allDoctors);
                    updateSchema(allDoctors);
                })
                .catch(err => {
                    console.warn('Fetch failed, using embedded data:', err);
                    if (data && data.doctors) {
                        allDoctors = data.doctors;
                        renderDoctors(allDoctors);
                        updateSchema(allDoctors);
                    } else {
                        grid.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">ডাক্তারদের তথ্য লোড করতে সমস্যা হচ্ছে।</p>';
                    }
                });
            
            function renderDoctors(doctors) {
                const html = doctors.map(d => `
                    <article class="doctor-card" 
                             data-department="${d.department || 'other'}" 
                             data-name="${d.name_en} ${d.name_bn}"
                             data-specialty="${(d.specialties_en || []).join(' ')} ${(d.specialties_bn || []).join(' ')} ${d.department_bn} ${d.qualifications.join(' ')}"
                             itemscope 
                             itemtype="https://schema.org/Physician">
                        <link itemprop="url" href="doctors/${d.slug}.html">
                        <meta itemprop="medicalSpecialty" content="${(d.specialties_en || []).join(', ')}">
                        <div class="doctor-avatar">
                            <img src="${d.image}" alt="${d.name_en}" itemprop="image" loading="lazy" onerror="this.onerror=null; this.src='${d.image_placeholder}';">
                        </div>
                        <h3 itemprop="name">
                            ${d.name_bn}
                            ${d.verified ? '<i class="fa-solid fa-circle-check" style="color: #1877f2; font-size: 0.7em; margin-left: 5px;" title="Verified"></i>' : ''}
                        </h3>
                        <span class="specialty" itemprop="jobTitle">${d.specialties_bn[0] || d.department_bn}</span>
                        <p class="degrees">${d.qualifications.join(', ')}</p>
                        <p style="font-size: 0.85rem; color: #555; margin: 0.5rem 0;">
                            <i class="fa-solid fa-hospital" style="color: var(--clr-primary);"></i>
                            ${d.affiliation_en}
                        </p>
                        <div class="schedule">
                            <i class="fa-regular fa-clock"></i>
                            <span>${d.schedule.day_bn} ${d.schedule.time_bn}</span>
                        </div>
                        <a href="doctors/${d.slug}.html" class="btn btn-primary" aria-label="View ${d.name_en} profile">
                            <i class="fa-solid fa-user-doctor"></i> প্রোফাইল দেখুন
                        </a>
                    </article>
                `).join('');
                grid.innerHTML = html;
            }
            
            function updateSchema(doctors) {
                const schemaScript = document.querySelector('script[type="application/ld+json"]');
                if (!schemaScript) return;
                try {
                    const schema = JSON.parse(schemaScript.textContent);
                    schema.itemListElement = doctors.map((d, i) => ({
                        "@type": "ListItem",
                        "position": i + 1,
                        "url": `https://greenhospitalbd.com/doctors/${d.slug}.html`,
                        "name": d.name_en
                    }));
                    schemaScript.textContent = JSON.stringify(schema, null, 2);
                } catch(e) {}
            }
            
            // Use embedded data immediately for instant render
            if (data && data.doctors) {
                allDoctors = data.doctors;
                renderDoctors(allDoctors);
                updateSchema(allDoctors);
            }
        })();
    </script>'''

content = re.sub(
    r'<script>\s*document\.getElementById\(\'currentYear\'\)\.textContent.*?</script>',
    new_doctors_js,
    content,
    flags=re.DOTALL
)
with open(BASE_DIR / "doctors.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK Updated doctors.html JS")

# Update services.html
with open(BASE_DIR / "services.html", "r", encoding="utf-8") as f:
    content = f.read()

new_services_js = '''    <script>
        document.getElementById('currentYear').textContent = new Date().getFullYear();
        
        // Load services with embedded data + fetch fallback
        (function loadServices() {
            const grid = document.getElementById('servicesGrid');
            const facGrid = document.getElementById('facilitiesGrid');
            let data = null;
            
            // Try embedded data first
            const embedded = document.getElementById('services-data');
            if (embedded) {
                try { data = JSON.parse(embedded.textContent); } catch(e) {}
            }
            
            // Try fetch as update
            fetch('data/services.json')
                .then(r => r.json())
                .then(fetched => render(fetched))
                .catch(() => { if (data) render(data); else if (grid) grid.innerHTML = '<p style="text-align:center;color:#999;">Services unavailable</p>'; });
            
            function render(d) {
                if (!d || !d.services) return;
                if (grid) {
                    grid.innerHTML = d.services.map(s => `
                        <div class="service-card" itemscope itemtype="https://schema.org/Service">
                            <meta itemprop="serviceType" content="${s.name_en}">
                            <i class="fa-solid ${s.icon}"></i>
                            <h3 class="service-title" itemprop="name">${s.name_bn}</h3>
                            <p itemprop="description">${s.description_bn}</p>
                            ${s.head_doctor ? `<p style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--clr-primary);"><i class="fa-solid fa-user-md"></i> ${s.head_doctor}</p>` : ''}
                        </div>
                    `).join('');
                }
                if (facGrid && d.facilities) {
                    facGrid.innerHTML = d.facilities.map(f => `
                        <div class="why-card">
                            <i class="fa-solid ${f.icon}"></i>
                            <h3>${f.name_bn}</h3>
                            <p>${f.description_bn}</p>
                            ${f.count ? `<p style="margin-top: 0.5rem; font-weight: 700; color: var(--clr-primary); font-size: 1.1rem;">${f.count} টি</p>` : ''}
                        </div>
                    `).join('');
                }
            }
            
            if (data) render(data);
        })();
    </script>'''

content = re.sub(
    r'<script>\s*document\.getElementById\(\'currentYear\'\)\.textContent.*?</script>',
    new_services_js,
    content,
    flags=re.DOTALL
)
with open(BASE_DIR / "services.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK Updated services.html JS")

# Update contact.html - load doctors for the dropdown
with open(BASE_DIR / "contact.html", "r", encoding="utf-8") as f:
    content = f.read()

new_contact_js = '''    <script>
        document.getElementById('currentYear').textContent = new Date().getFullYear();
        
        // Set min date to today
        document.getElementById('appointment_date').min = new Date().toISOString().split('T')[0];
        
        // Load doctors for select with embedded data + fetch fallback
        (function loadDoctorOptions() {
            const select = document.getElementById('doctor');
            const optgroup = select.querySelector('optgroup');
            let data = null;
            
            // Try embedded data first
            const embedded = document.getElementById('doctors-data');
            if (embedded) {
                try { data = JSON.parse(embedded.textContent); } catch(e) {}
            }
            
            // Try fetch as update
            fetch('data/doctors.json')
                .then(r => r.json())
                .then(fetched => renderOptions(fetched))
                .catch(() => { if (data) renderOptions(data); });
            
            function renderOptions(d) {
                if (!d || !d.doctors) return;
                optgroup.innerHTML = d.doctors.map(doc => 
                    `<option value="${doc.id}">${doc.name_en} - ${doc.specialties_en[0] || doc.department_bn}</option>`
                ).join('');
            }
            
            if (data) renderOptions(data);
        })();
    </script>'''

content = re.sub(
    r'<script>\s*document\.getElementById\(\'currentYear\'\)\.textContent.*?</script>',
    new_contact_js,
    content,
    flags=re.DOTALL
)
with open(BASE_DIR / "contact.html", "w", encoding="utf-8") as f:
    f.write(content)
print("OK Updated contact.html JS")

print("\nAll pages updated with embedded data + fetch fallback!")
