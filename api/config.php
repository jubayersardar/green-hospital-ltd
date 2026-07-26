<?php
/**
 * Faridpur Green Hospital - Configuration
 * 
 * Edit these values for your production environment.
 * Keep this file OUTSIDE the public html directory if possible.
 */

// Hospital Information
define('HOSPITAL_NAME', 'Faridpur Green Hospital Ltd');
define('HOSPITAL_NAME_BN', 'ফরিদপুর গ্রিন হাসপাতাল লিমিটেড');
define('HOSPITAL_ADDRESS', 'Kabi Jasim Uddin Road, Alipur, Faridpur Sadar, Faridpur');
define('HOSPITAL_PHONE', '+8801988118833');
define('HOSPITAL_EMAIL', 'info@greenhospitalbd.com');
define('HOSPITAL_FACEBOOK', 'https://www.facebook.com/p/Faridpur-Green-Hospital-Ltd-100067848113453/');
define('HOSPITAL_WEBSITE', 'https://greenhospitalbd.com/');

// Email Configuration
define('NOTIFICATION_EMAIL', 'info@greenhospitalbd.com');
define('FROM_EMAIL', 'noreply@greenhospitalbd.com');
define('FROM_NAME', 'Green Hospital Website');

// Admin Panel
define('ADMIN_USERNAME', 'admin');
define('ADMIN_PASSWORD_HASH', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'); // Default: "GreenHospital2026!" - CHANGE THIS!

// Storage
define('STORAGE_DIR', __DIR__ . '/../data/submissions/');

// Security
define('CSRF_TOKEN_NAME', 'ghl_csrf_token');
define('SESSION_NAME', 'ghl_admin_session');

// Application
define('APP_VERSION', '1.0.0');
define('DEBUG_MODE', false);

// Timezone
date_default_timezone_set('Asia/Dhaka');
