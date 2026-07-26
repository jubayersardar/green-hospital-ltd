<?php
/**
 * Contact Form Handler
 * Faridpur Green Hospital Ltd
 * 
 * Handles contact form submissions, validates data, logs to JSON, sends email
 */

// ===== Security Headers =====
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');

// ===== Only allow POST =====
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// ===== Configuration =====
$TO_EMAIL = 'info@greenhospitalbd.com';
$FROM_EMAIL = 'noreply@greenhospitalbd.com';
$HOSPITAL_NAME = 'Faridpur Green Hospital Ltd';
$STORAGE_DIR = __DIR__ . '/../data/submissions/';

// ===== Rate Limiting (simple file-based) =====
$ip = $_SERVER['REMOTE_ADDR'];
$rate_limit_file = sys_get_temp_dir() . '/ghl_rate_' . md5($ip);
if (file_exists($rate_limit_file) && (time() - filemtime($rate_limit_file)) < 60) {
    $last = (int)file_get_contents($rate_limit_file);
    if ($last >= 3) {
        http_response_code(429);
        echo json_encode([
            'success' => false,
            'message' => 'অতিরিক্ত অনুরোধ। অনুগ্রহ করে ১ মিনিট অপেক্ষা করুন।'
        ]);
        exit;
    }
    file_put_contents($rate_limit_file, $last + 1);
} else {
    file_put_contents($rate_limit_file, 1);
}

// ===== Sanitize & Validate Input =====
function sanitize($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

function validatePhone($phone) {
    // Bangladesh phone: 01XXXXXXXXX (11 digits, starts with 01)
    $phone = preg_replace('/[^0-9]/', '', $phone);
    return preg_match('/^01[3-9][0-9]{8}$/', $phone);
}

$name = sanitize($_POST['name'] ?? '');
$phone = sanitize($_POST['phone'] ?? '');
$email = sanitize($_POST['email'] ?? '');
$department = sanitize($_POST['department'] ?? 'general');
$message = sanitize($_POST['message'] ?? '');

// Validation
$errors = [];

if (empty($name) || mb_strlen($name) < 2 || mb_strlen($name) > 100) {
    $errors[] = 'অনুগ্রহ করে সঠিক নাম লিখুন (২-১০০ অক্ষর)।';
}

if (empty($phone) || !validatePhone($phone)) {
    $errors[] = 'অনুগ্রহ করে সঠিক মোবাইল নম্বর লিখুন (01XXXXXXXXX)।';
}

if (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'অনুগ্রহ করে সঠিক ইমেইল ঠিকানা লিখুন।';
}

if (mb_strlen($message) > 2000) {
    $errors[] = 'বার্তা ২০০০ অক্ষরের বেশি হতে পারবে না।';
}

// ===== Honeypot check (anti-spam) =====
if (!empty($_POST['website']) || !empty($_POST['url'])) {
    // Bot detected, silently succeed
    echo json_encode(['success' => true, 'message' => 'বার্তা পাঠানো হয়েছে।']);
    exit;
}

if (!empty($errors)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => implode(' ', $errors)
    ]);
    exit;
}

// ===== Save to JSON =====
if (!is_dir($STORAGE_DIR)) {
    @mkdir($STORAGE_DIR, 0755, true);
}

$submission = [
    'id' => uniqid('c_', true),
    'type' => 'contact',
    'name' => $name,
    'phone' => $phone,
    'email' => $email,
    'department' => $department,
    'message' => $message,
    'ip' => $ip,
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? '',
    'created_at' => date('Y-m-d H:i:s'),
    'status' => 'new'
];

$contacts_file = $STORAGE_DIR . 'contacts.json';
$existing = [];
if (file_exists($contacts_file)) {
    $content = file_get_contents($contacts_file);
    $existing = json_decode($content, true) ?: [];
}
$existing[] = $submission;
$save_result = @file_put_contents($contacts_file, json_encode($existing, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

// ===== Send Email =====
$email_sent = false;
$subject = "[Website] নতুন বার্তা: {$name}";
$email_body = "
নতুন যোগাযোগ ফর্ম জমা:

নাম: {$name}
ফোন: {$phone}
ইমেইল: {$email}
বিভাগ: {$department}
সময়: " . date('Y-m-d H:i:s') . "

বার্তা:
{$message}

---
IP: {$ip}
User Agent: " . ($_SERVER['HTTP_USER_AGENT'] ?? 'N/A') . "
";

$headers = [
    'From: ' . $HOSPITAL_NAME . ' <' . $FROM_EMAIL . '>',
    'Reply-To: ' . $email,
    'X-Mailer: PHP/' . phpversion(),
    'Content-Type: text/plain; charset=UTF-8'
];

if (function_exists('mail')) {
    $email_sent = @mail($TO_EMAIL, $subject, $email_body, implode("\r\n", $headers));
}

// ===== Send WhatsApp Notification (optional) =====
$whatsapp_sent = false;
$whatsapp_api_url = ''; // Add your WhatsApp API URL here if available

// ===== Response =====
$response = [
    'success' => true,
    'message' => 'আপনার বার্তা সফলভাবে পাঠানো হয়েছে। আমাদের টিম শিঘ্রই আপনার সাথে যোগাযোগ করবে।',
    'data' => [
        'id' => $submission['id'],
        'saved' => $save_result !== false,
        'email_sent' => $email_sent
    ]
];

http_response_code(200);
echo json_encode($response, JSON_UNESCAPED_UNICODE);
exit;
