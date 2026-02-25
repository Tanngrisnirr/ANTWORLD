<?php
/**
 * ANTWORLD Dashboard Data API
 * Returns project metrics as JSON for dashboard auto-refresh
 */

header('Content-Type: application/json');
header('Cache-Control: no-cache, must-revalidate');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');

// Base paths
$alphaDir = dirname(__DIR__);
$baseDir = dirname($alphaDir);

/**
 * Calculate directory size in KB
 */
function getDirSize($dir) {
    $size = 0;
    if (is_dir($dir)) {
        foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS)) as $file) {
            if ($file->isFile()) {
                $size += $file->getSize();
            }
        }
    }
    return round($size / 1024);
}

/**
 * Get file stats by extension (count and size in KB)
 */
function getFileStatsByType($dir, $extensions) {
    $stats = [];
    foreach ($extensions as $ext) {
        $stats[$ext] = ['count' => 0, 'size_kb' => 0];
    }
    $stats['other'] = ['count' => 0, 'size_kb' => 0];

    if (!is_dir($dir)) return $stats;

    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS)) as $file) {
        if ($file->isFile()) {
            $ext = strtolower(pathinfo($file->getFilename(), PATHINFO_EXTENSION));
            $size = $file->getSize() / 1024; // KB
            if (isset($stats[$ext])) {
                $stats[$ext]['count']++;
                $stats[$ext]['size_kb'] += $size;
            } else {
                $stats['other']['count']++;
                $stats['other']['size_kb'] += $size;
            }
        }
    }

    // Round sizes
    foreach ($stats as &$s) {
        $s['size_kb'] = round($s['size_kb'], 1);
    }
    return $stats;
}

/**
 * Get image asset stats (count and size in KB)
 */
function getImageAssetStats($dir) {
    $stats = [
        'jpg' => ['count' => 0, 'size_kb' => 0],
        'png' => ['count' => 0, 'size_kb' => 0],
        'svg' => ['count' => 0, 'size_kb' => 0],
        'webp' => ['count' => 0, 'size_kb' => 0],
        'gif' => ['count' => 0, 'size_kb' => 0]
    ];

    if (!is_dir($dir)) return $stats;

    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS)) as $file) {
        if ($file->isFile()) {
            $ext = strtolower(pathinfo($file->getFilename(), PATHINFO_EXTENSION));
            if ($ext === 'jpeg') $ext = 'jpg';
            $size = $file->getSize() / 1024; // KB
            if (isset($stats[$ext])) {
                $stats[$ext]['count']++;
                $stats[$ext]['size_kb'] += $size;
            }
        }
    }

    // Round sizes
    foreach ($stats as &$s) {
        $s['size_kb'] = round($s['size_kb'], 1);
    }
    return $stats;
}

/**
 * Count content items
 */
function countContent($alphaDir) {
    $content = [
        'Species Pages' => 0,
        'ID Pages' => 0,
        'Morpho SVGs' => 0,
        'Photo Assets' => 0,
        'Icon Assets' => 0
    ];

    // Count ID pages
    $idDir = $alphaDir . '/id';
    if (is_dir($idDir)) {
        foreach (glob($idDir . '/*.html') as $file) {
            $content['ID Pages']++;
        }
    }

    // Count morpho SVGs
    $morphoSvgDir = $alphaDir . '/img/morpho/svg';
    if (is_dir($morphoSvgDir)) {
        foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($morphoSvgDir, RecursiveDirectoryIterator::SKIP_DOTS)) as $file) {
            if ($file->isFile() && strtolower(pathinfo($file->getFilename(), PATHINFO_EXTENSION)) === 'svg') {
                $content['Morpho SVGs']++;
            }
        }
    }

    // Count photo assets
    $photoDir = $alphaDir . '/img/photo';
    if (is_dir($photoDir)) {
        foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($photoDir, RecursiveDirectoryIterator::SKIP_DOTS)) as $file) {
            if ($file->isFile()) {
                $content['Photo Assets']++;
            }
        }
    }

    // Count icon assets
    $iconDir = $alphaDir . '/icon';
    if (is_dir($iconDir)) {
        foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($iconDir, RecursiveDirectoryIterator::SKIP_DOTS)) as $file) {
            if ($file->isFile()) {
                $content['Icon Assets']++;
            }
        }
    }

    // Count species (from list_species.html or similar)
    $speciesFile = $alphaDir . '/list_species.html';
    if (file_exists($speciesFile)) {
        $speciesContent = file_get_contents($speciesFile);
        // Count table rows or species entries
        preg_match_all('/<tr[^>]*class="[^"]*species[^"]*"/', $speciesContent, $matches);
        $content['Species Pages'] = count($matches[0]);
        if ($content['Species Pages'] === 0) {
            // Alternative: count data rows
            preg_match_all('/<tr[^>]*>/', $speciesContent, $matches);
            $content['Species Pages'] = max(0, count($matches[0]) - 1); // Subtract header row
        }
    }

    return $content;
}

/**
 * Get recent git commits
 */
function getRecentCommits($baseDir, $limit = 10) {
    $commits = [];
    $gitDir = dirname($baseDir); // ANTWORLD root

    $cmd = "cd " . escapeshellarg($gitDir) . " && git log --oneline -n " . intval($limit) . " --format='%h|%ad|%s' --date=short 2>/dev/null";
    $output = shell_exec($cmd);

    if ($output) {
        foreach (explode("\n", trim($output)) as $line) {
            if (empty($line)) continue;
            $parts = explode('|', $line, 3);
            if (count($parts) === 3) {
                $commits[] = [
                    'hash' => $parts[0],
                    'date' => $parts[1],
                    'message' => $parts[2]
                ];
            }
        }
    }
    return $commits;
}

/**
 * Get recently modified files
 */
function getRecentModifications($dir, $limit = 15) {
    $files = [];
    $skipDirs = ['backup_svg', '.git', 'node_modules'];

    if (!is_dir($dir)) return $files;

    foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS)) as $file) {
        // Skip backup directories
        $path = $file->getPathname();
        $skip = false;
        foreach ($skipDirs as $skipDir) {
            if (strpos($path, '/' . $skipDir . '/') !== false) {
                $skip = true;
                break;
            }
        }
        if ($skip) continue;

        if ($file->isFile()) {
            $relativePath = str_replace($dir . '/', '', $path);
            $files[] = [
                'file' => $relativePath,
                'modified' => date('Y-m-d H:i', $file->getMTime()),
                'size' => formatFileSize($file->getSize()),
                'mtime' => $file->getMTime()
            ];
        }
    }

    // Sort by modification time, newest first
    usort($files, function($a, $b) {
        return $b['mtime'] - $a['mtime'];
    });

    // Remove mtime from output and limit
    $result = [];
    foreach (array_slice($files, 0, $limit) as $f) {
        unset($f['mtime']);
        $result[] = $f;
    }

    return $result;
}

/**
 * Format file size
 */
function formatFileSize($bytes) {
    if ($bytes >= 1048576) return round($bytes / 1048576, 1) . ' MB';
    if ($bytes >= 1024) return round($bytes / 1024, 1) . ' KB';
    return $bytes . ' B';
}

/**
 * Load project history from JSON file
 */
function loadProjectHistory($alphaDir) {
    $historyFile = $alphaDir . '/php/dashboard_history.json';
    if (file_exists($historyFile)) {
        $data = json_decode(file_get_contents($historyFile), true);
        return $data['projectHistory'] ?? [];
    }
    return [];
}

/**
 * Load git commits from JSON file (since container can't access git)
 */
function loadGitCommits($alphaDir) {
    $historyFile = $alphaDir . '/php/dashboard_history.json';
    if (file_exists($historyFile)) {
        $data = json_decode(file_get_contents($historyFile), true);
        return $data['recentCommits'] ?? [];
    }
    return [];
}

// Build response data
$codeExts = ['html', 'htm', 'css', 'js', 'php', 'svg', 'json', 'txt', 'pdf', 'png', 'jpg', 'gif', 'xml'];

$data = [
    'lastUpdate' => date('Y-m-d H:i:s'),
    'projectSize' => [
        'alpha_kb' => getDirSize($alphaDir),
        'beta_kb' => getDirSize($baseDir . '/beta'),
        'delta_kb' => getDirSize($baseDir . '/delta'),
        'total_kb' => getDirSize($baseDir)
    ],
    'fileTypes' => getFileStatsByType($alphaDir, $codeExts),
    'content' => countContent($alphaDir),
    'imageAssets' => getImageAssetStats($alphaDir),
    'projectHistory' => loadProjectHistory($alphaDir),
    'recentCommits' => getRecentCommits($baseDir) ?: loadGitCommits($alphaDir),
    'recentModifications' => getRecentModifications($alphaDir)
];

// If no history, create initial entry
if (empty($data['projectHistory'])) {
    $data['projectHistory'] = [
        ['date' => date('Y-m-d'), 'size_kb' => $data['projectSize']['alpha_kb'], 'notes' => 'Initial']
    ];
}

echo json_encode($data, JSON_PRETTY_PRINT);
