<?php
/**
 * AJAX endpoint to set language cookie
 * POST: { "lang": "en" | "fr" | "zh" }
 */

header('Content-Type: application/json');

$allowed = ['en', 'fr', 'zh'];

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}


$input = json_decode(file_get_contents('php://input'), true);
$lang = isset($input['lang']) ? $input['lang'] : null;


if (!$lang && isset($_POST['lang'])) {
    $lang = $_POST['lang'];
}

if (!$lang || !in_array($lang, $allowed)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid language', 'allowed' => $allowed]);
    exit;
}


$expiry = time() + (365 * 24 * 60 * 60);
setcookie('aw_lang', $lang, [
    'expires' => $expiry,
    'path' => '/',
    'secure' => isset($_SERVER['HTTPS']),
    'httponly' => false,
    'samesite' => 'Lax'
]);

echo json_encode(['success' => true, 'lang' => $lang]);
