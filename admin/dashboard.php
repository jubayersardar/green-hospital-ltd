<?php
/**
 * Admin Dashboard
 */
session_start();
require_once __DIR__ . '/../api/config.php';

// Check auth
if (empty($_SESSION['admin_logged_in'])) {
    header('Location: login.html');
    exit;
}

// Session timeout (30 min)
if (time() - ($_SESSION['login_time'] ?? 0) > 1800) {
    session_destroy();
    header('Location: login.html');
    exit;
}

// Load submissions
$contacts_file = STORAGE_DIR . 'contacts.json';
$appointments_file = STORAGE_DIR . 'appointments.json';

$contacts = file_exists($contacts_file) ? json_decode(file_get_contents($contacts_file), true) ?: [] : [];
$appointments = file_exists($appointments_file) ? json_decode(file_get_contents($appointments_file), true) ?: [] : [];

// Sort by date desc
usort($contacts, fn($a, $b) => strcmp($b['created_at'] ?? '', $a['created_at'] ?? ''));
usort($appointments, fn($a, $b) => strcmp($b['created_at'] ?? '', $a['created_at'] ?? ''));

$active_tab = $_GET['tab'] ?? 'appointments';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <title>Admin Dashboard - Green Hospital</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #f5f7fa; color: #1a1f36; }
        .header { background: #0a8d4a; color: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .header h1 { font-size: 1.25rem; }
        .header a { color: white; text-decoration: none; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 1.5rem; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .stat-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        .stat-card h3 { color: #6b7280; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.5rem; }
        .stat-card .value { font-size: 2rem; font-weight: 700; color: #0a8d4a; }
        .tabs { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; border-bottom: 2px solid #e5e7eb; }
        .tab { padding: 0.75rem 1.5rem; background: none; border: none; cursor: pointer; color: #6b7280; font-weight: 600; border-bottom: 3px solid transparent; margin-bottom: -2px; }
        .tab.active { color: #0a8d4a; border-bottom-color: #0a8d4a; }
        .data-table { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        .data-table table { width: 100%; border-collapse: collapse; }
        .data-table th { background: #f9fafb; padding: 1rem; text-align: left; font-size: 0.85rem; color: #6b7280; text-transform: uppercase; font-weight: 600; }
        .data-table td { padding: 1rem; border-top: 1px solid #f3f4f6; font-size: 0.9rem; }
        .data-table tr:hover { background: #f9fafb; }
        .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
        .badge-new { background: #fef3c7; color: #92400e; }
        .badge-pending { background: #dbeafe; color: #1e40af; }
        .badge-done { background: #d1fae5; color: #065f46; }
        .empty { text-align: center; padding: 3rem; color: #9ca3af; }
        .empty i { font-size: 3rem; margin-bottom: 1rem; }
        @media (max-width: 768px) {
            .data-table { overflow-x: auto; }
            .header { padding: 1rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fa-solid fa-hospital"></i> Green Hospital Admin</h1>
        <div>
            <span style="margin-right: 1rem; font-size: 0.9rem;"><i class="fa-solid fa-user"></i> <?= htmlspecialchars($_SESSION['admin_user']) ?></span>
            <a href="logout.php"><i class="fa-solid fa-right-from-bracket"></i> Logout</a>
        </div>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3>Total Appointments</h3>
                <div class="value"><?= count($appointments) ?></div>
            </div>
            <div class="stat-card">
                <h3>Pending</h3>
                <div class="value" style="color: #d97706;"><?= count(array_filter($appointments, fn($a) => ($a['status'] ?? '') === 'pending')) ?></div>
            </div>
            <div class="stat-card">
                <h3>Total Contacts</h3>
                <div class="value" style="color: #1877f2;"><?= count($contacts) ?></div>
            </div>
            <div class="stat-card">
                <h3>New Messages</h3>
                <div class="value" style="color: #d97706;"><?= count(array_filter($contacts, fn($c) => ($c['status'] ?? '') === 'new')) ?></div>
            </div>
        </div>
        
        <div class="tabs">
            <a href="?tab=appointments" style="text-decoration:none;"><button class="tab <?= $active_tab === 'appointments' ? 'active' : '' ?>">Appointments (<?= count($appointments) ?>)</button></a>
            <a href="?tab=contacts" style="text-decoration:none;"><button class="tab <?= $active_tab === 'contacts' ? 'active' : '' ?>">Contacts (<?= count($contacts) ?>)</button></a>
        </div>
        
        <div class="data-table">
            <?php if ($active_tab === 'appointments'): ?>
                <?php if (empty($appointments)): ?>
                    <div class="empty">
                        <i class="fa-regular fa-calendar"></i>
                        <p>No appointments yet</p>
                    </div>
                <?php else: ?>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Phone</th>
                                <th>Doctor/Dept</th>
                                <th>Date</th>
                                <th>Status</th>
                                <th>Submitted</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($appointments as $a): ?>
                                <tr>
                                    <td><code><?= htmlspecialchars($a['id'] ?? '') ?></code></td>
                                    <td><?= htmlspecialchars($a['name'] ?? '') ?></td>
                                    <td><a href="tel:<?= htmlspecialchars($a['phone'] ?? '') ?>"><?= htmlspecialchars($a['phone'] ?? '') ?></a></td>
                                    <td><?= htmlspecialchars($a['doctor'] ?? '') ?></td>
                                    <td><?= htmlspecialchars($a['appointment_date'] ?? 'Any') ?></td>
                                    <td><span class="badge badge-<?= htmlspecialchars($a['status'] ?? 'pending') ?>"><?= htmlspecialchars($a['status'] ?? 'pending') ?></span></td>
                                    <td><?= htmlspecialchars($a['created_at'] ?? '') ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                <?php endif; ?>
            <?php else: ?>
                <?php if (empty($contacts)): ?>
                    <div class="empty">
                        <i class="fa-regular fa-envelope"></i>
                        <p>No contact messages yet</p>
                    </div>
                <?php else: ?>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Phone</th>
                                <th>Email</th>
                                <th>Dept</th>
                                <th>Message</th>
                                <th>Status</th>
                                <th>Submitted</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($contacts as $c): ?>
                                <tr>
                                    <td><?= htmlspecialchars($c['name'] ?? '') ?></td>
                                    <td><a href="tel:<?= htmlspecialchars($c['phone'] ?? '') ?>"><?= htmlspecialchars($c['phone'] ?? '') ?></a></td>
                                    <td><?= htmlspecialchars($c['email'] ?? '-') ?></td>
                                    <td><?= htmlspecialchars($c['department'] ?? '-') ?></td>
                                    <td style="max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="<?= htmlspecialchars($c['message'] ?? '') ?>"><?= htmlspecialchars($c['message'] ?? '-') ?></td>
                                    <td><span class="badge badge-<?= htmlspecialchars($c['status'] ?? 'new') ?>"><?= htmlspecialchars($c['status'] ?? 'new') ?></span></td>
                                    <td><?= htmlspecialchars($c['created_at'] ?? '') ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                <?php endif; ?>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
