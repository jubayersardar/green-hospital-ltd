<?php
/**
 * Admin Authentication
 */
session_start();
header('Content-Type: application/json; charset=utf-8');

require_once __DIR__ . '/../api/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

$username = trim($_POST['username'] ?? '');
$password = $_POST['password'] ?? '';

if (empty($username) || empty($password)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Username and password required']);
    exit;
}

// Verify credentials
if ($username === ADMIN_USERNAME && password_verify($password, ADMIN_PASSWORD_HASH)) {
    // Regenerate session ID
    session_regenerate_id(true);
    $_SESSION['admin_logged_in'] = true;
    $_SESSION['admin_user'] = $username;
    $_SESSION['login_time'] = time();
    
    echo json_encode(['success' => true, 'message' => 'Login successful']);
    exit;
}

// Generic error (don't reveal which field is wrong)
http_response_code(401);
echo json_encode(['success' => false, 'message' => 'Invalid username or password']);
