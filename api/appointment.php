<?php
/**
 * Appointment Booking Handler
 * Faridpur Green Hospital Ltd
 */
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

$TO_EMAIL = 'info@greenhospitalbd.com';
$FROM_EMAIL = 'noreply@greenhospitalbd.com';
$HOSPITAL_NAME = 'Faridpur Green Hospital Ltd';
$STORAGE_DIR = __DIR__ . '/../data/submissions/';

// Rate limiting
$ip = $_SERVER['REMOTE_ADDR'];
$rate_limit_file = sys_get_temp_dir() . '/ghl_appt_' . md5($ip);
if (file_exists($rate_limit_file) && (time() - filemtime($rate_limit_file)) < 120) {
    $last = (int)file_get_contents($rate_limit_file);
    if ($last >= 5) {
        http_response_code(429);
        echo json_encode([
            'success' => false,
            'message' => 'অতিরিক্ত অনুরোধ। ২ মিনিট অপেক্ষা করে আবার চেষ্টা করুন।'
        ]);
        exit;
    }
    file_put_contents($rate_limit_file, $last + 1);
} else {
    file_put_contents($rate_limit_file, 1);
}

function sanitize($data) {
    return htmlspecialchars(trim(stripslashes($data)), ENT_QUOTES, 'UTF-8');
}

$name = sanitize($_POST['name'] ?? '');
$phone = sanitize($_POST['phone'] ?? '');
$email = sanitize($_POST['email'] ?? '');
$doctor = sanitize($_POST['doctor'] ?? '');
$date = sanitize($_POST['appointment_date'] ?? '');
$message = sanitize($_POST['message'] ?? '');

$errors = [];
if (empty($name) || mb_strlen($name) < 2) $errors[] = 'সঠিক নাম আবশ্যক।';
$phone_clean = preg_replace('/[^0-9]/', '', $phone);
if (!preg_match('/^01[3-9][0-9]{8}$/', $phone_clean)) $errors[] = 'সঠিক মোবাইল নম্বর আবশ্যক।';
if (empty($doctor)) $errors[] = 'ডাক্তার/বিভাগ নির্বাচন আবশ্যক।';
if (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'সঠিক ইমেইল প্রদান করুন।';
if (!empty($date)) {
    $d = DateTime::createFromFormat('Y-m-d', $date);
    if (!$d || $d->format('Y-m-d') !== $date) $errors[] = 'সঠিক তারিখ দিন।';
    if ($d && $d < new DateTime('today')) $errors[] = 'অনুগ্রহ করে ভবিষ্যৎ তারিখ নির্বাচন করুন।';
}

// Honeypot
if (!empty($_POST['website']) || !empty($_POST['url'])) {
    echo json_encode(['success' => true, 'message' => 'অ্যাপয়েন্টমেন্ট গ্রহণ করা হয়েছে।']);
    exit;
}

if (!empty($errors)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => implode(' ', $errors)]);
    exit;
}

if (!is_dir($STORAGE_DIR)) @mkdir($STORAGE_DIR, 0755, true);

$appointment = [
    'id' => 'APT-' . strtoupper(uniqid()),
    'type' => 'appointment',
    'name' => $name,
    'phone' => $phone_clean,
    'email' => $email,
    'doctor' => $doctor,
    'appointment_date' => $date,
    'message' => $message,
    'ip' => $ip,
    'created_at' => date('Y-m-d H:i:s'),
    'status' => 'pending',
    'priority' => 'normal'
];

$appointments_file = $STORAGE_DIR . 'appointments.json';
$existing = [];
if (file_exists($appointments_file)) {
    $content = file_get_contents($appointments_file);
    $existing = json_decode($content, true) ?: [];
}
$existing[] = $appointment;
@file_put_contents($appointments_file, json_encode($existing, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

// Send email
$subject = "[Appointment] নতুন অ্যাপয়েন্টমেন্ট - {$name} - {$appointment['id']}";
$body = "
নতুন অ্যাপয়েন্টমেন্ট বুকিং

অ্যাপয়েন্টমেন্ট আইডি: {$appointment['id']}

রোগীর নাম: {$name}
মোবাইল: {$phone_clean}
ইমেইল: {$email}
ডাক্তার/বিভাগ: {$doctor}
পছন্দের তারিখ: {$date}

বার্তা: {$message}

জমা দেওয়ার সময়: " . date('Y-m-d H:i:s') . "
IP: {$ip}

---
$HOSPITAL_NAME - অ্যাপয়েন্টমেন্ট সিস্টেম
";

$headers = [
    'From: ' . $HOSPITAL_NAME . ' <' . $FROM_EMAIL . '>',
    'Reply-To: ' . ($email ?: $FROM_EMAIL),
    'Content-Type: text/plain; charset=UTF-8'
];

$email_sent = false;
if (function_exists('mail')) {
    $email_sent = @mail($TO_EMAIL, $subject, $body, implode("\r\n", $headers));
}

echo json_encode([
    'success' => true,
    'message' => "অ্যাপয়েন্টমেন্ট আইডি: {$appointment['id']}। আমরা শিঘ্রই আপনার সাথে যোগাযোগ করবো। জরুরি হলে সরাসরি কল করুন: 01988-118833",
    'data' => [
        'appointment_id' => $appointment['id'],
        'email_sent' => $email_sent
    ]
], JSON_UNESCAPED_UNICODE);
