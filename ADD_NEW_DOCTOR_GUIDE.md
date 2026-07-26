# How to Add a New Doctor to the Website

> Simple step-by-step guide for the admin to add new doctor profiles.

## Method 1: Edit JSON (Recommended) ⭐

### Step 1: Open the doctors.json file
```bash
# File location:
D:\minimax\New folder\Green Hospital Ltd\data\doctors.json
```

### Step 2: Add a new doctor object
Copy this template and paste it before the closing `]` of the `doctors` array:

```json
{
  "id": "doctor-unique-slug",
  "slug": "doctor-unique-slug",
  "name_bn": "ডা. নতুন ডাক্তার",
  "name_en": "Dr. New Doctor",
  "title": "Doctor",
  "designation_bn": "বিশেষজ্ঞতার নাম",
  "designation_en": "Specialty Name",
  "affiliation_bn": "প্রতিষ্ঠানের নাম",
  "affiliation_en": "Affiliation Name",
  "qualifications": [
    "MBBS",
    "FCPS"
  ],
  "specialties_bn": ["বিশেষজ্ঞতা ১"],
  "specialties_en": ["Specialty 1"],
  "expertise": [
    "Skill 1",
    "Skill 2"
  ],
  "department": "cardiology",
  "department_bn": "কার্ডিওলজি",
  "experience_years": 10,
  "languages": ["Bangla", "English"],
  "schedule": {
    "day_en": "Every Monday",
    "day_bn": "প্রতি সোমবার",
    "time_en": "10:00 AM - 2:00 PM",
    "time_bn": "সকাল ১০:০০ - দুপুর ২:০০"
  },
  "serial_number": "01988-118833",
  "consultation_fee": "৫০০ টাকা",
  "image": "images/doctors/doctor-unique-slug.jpg",
  "image_placeholder": "https://placehold.co/600x600/0a8d4a/ffffff?text=Dr.+Name",
  "verified": true,
  "source": "Manual entry",
  "bio_bn": "ডাক্তার সম্পর্কে বাংলায়...",
  "bio_en": "Doctor bio in English..."
}
```

### Step 3: Add doctor photo
Save the photo as:
```
D:\minimax\New folder\Green Hospital Ltd\doctors\images\doctor-unique-slug.jpg
```
(Use same filename as the `image` field in JSON)

### Step 4: Generate profile page
```bash
cd "D:\minimax\New folder\Green Hospital Ltd"
python tools\generate_doctor_pages.py
```

### Step 5: Verify
Open `http://localhost:8000/doctors.html` to see the new doctor!

---

## Method 2: Use the Admin Panel

1. Go to `http://yoursite.com/admin/login.html`
2. Login with admin credentials
3. (Coming soon: Add Doctor form)

---

## Available Departments (for "department" field)

| Department Code | English Name | বাংলা নাম |
|----------------|--------------|-----------|
| `medicine` | Medicine | মেডিসিন |
| `cardiology` | Cardiology | কার্ডিওলজি |
| `gastroenterology` | Gastroenterology | গ্যাস্ট্রোএন্টারোলজি |
| `neurology` | Neurology | নিউরোলজি |
| `neurosurgery` | Neurosurgery | নিউরোসার্জারি |
| `orthopedics` | Orthopedics | অর্থোপেডিকস |
| `gynecology` | Gynecology & Obstetrics | গাইনি ও প্রসূতি |
| `dermatology` | Dermatology | চর্মরোগ |
| `dental` | Dental | ডেন্টাল |
| `ent` | ENT | নাক কান গলা |
| `eye` | Ophthalmology | চক্ষু |
| `pediatrics` | Pediatrics | শিশু রোগ |
| `urology` | Urology | ইউরোলজি |
| `homeopathy` | Homeopathy | হোমিওপ্যাথি |
| `surgery` | General Surgery | জেনারেল সার্জারি |
| `anesthesiology` | Anesthesiology | অ্যানেস্থেসিওলজি |
| `radiology` | Radiology | রেডিওলজি |
| `psychiatry` | Psychiatry | মানসিক রোগ |
| `ent` | ENT | নাক কান গলা |

---

## Field Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `id` | ✅ | Unique identifier (lowercase, hyphens) |
| `slug` | ✅ | URL-friendly version (e.g. `dr-md-rahim`) |
| `name_bn` | ✅ | Name in Bangla |
| `name_en` | ✅ | Name in English |
| `title` | ✅ | Dr., Professor, Associate Professor, etc. |
| `qualifications` | ✅ | Array of degrees |
| `specialties_*` | ✅ | At least one specialty |
| `department` | ✅ | One of the codes above |
| `schedule` | ✅ | Day and time |
| `image` | ✅ | Path to photo |
| `verified` | ✅ | `true` if data is verified |

---

## Common Tasks

### To change a doctor's photo:
1. Replace the file at `doctors/images/[slug].jpg`
2. Refresh browser (clear cache if needed)

### To remove a doctor:
1. Delete the doctor object from `doctors.json`
2. Delete `doctors/[slug].html`
3. Delete `doctors/images/[slug].jpg`

### To update existing doctor:
1. Edit the relevant fields in `doctors.json`
2. Run `python tools/generate_doctor_pages.py`

---

## Tips

- **Use high-quality photos** (min 600x600px, square)
- **Always include both Bangla and English** for name/bio
- **Add accurate data only** - mark `verified: false` if unsure
- **Test mobile view** after adding

---

## Need Help?

- **Phone**: 01988-118833
- **Email**: info@greenhospitalbd.com
- **For technical issues**: Contact website developer
