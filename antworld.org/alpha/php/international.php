<?php
/**
 * AntWorld Internationalization System
 * Handles language detection, loading, and translation
 */

// Global translations array
$GLOBALS['aw_translations'] = [];
$GLOBALS['aw_lang'] = null;

/**
 * Get current language from cookie, defaults to 'en'
 */
function get_current_lang() {
    if ($GLOBALS['aw_lang'] !== null) {
        return $GLOBALS['aw_lang'];
    }

    $allowed = ['en', 'fr', 'zh'];
    $lang = isset($_COOKIE['aw_lang']) ? $_COOKIE['aw_lang'] : 'en';

    if (!in_array($lang, $allowed)) {
        $lang = 'en';
    }

    $GLOBALS['aw_lang'] = $lang;
    return $lang;
}

/**
 * Shorthand for get_current_lang()
 */
function lang() {
    return get_current_lang();
}

/**
 * Load shared translations (nav, footer, ui)
 */
function load_translations() {
    $lang = get_current_lang();
    $file = __DIR__ . '/lang/' . $lang . '.json';

    if (file_exists($file)) {
        $content = file_get_contents($file);
        $translations = json_decode($content, true);
        if ($translations) {
            $GLOBALS['aw_translations'] = array_merge($GLOBALS['aw_translations'], $translations);
        }
    }
}

/**
 * Load page-specific translations
 * @param string $page Page name (e.g., 'index', 'morpho')
 */
function load_page_translations($page) {
    $lang = get_current_lang();
    $file = __DIR__ . '/lang/pages/' . $page . '.' . $lang . '.json';

    if (file_exists($file)) {
        $content = file_get_contents($file);
        $translations = json_decode($content, true);
        if ($translations) {
            $GLOBALS['aw_translations'] = array_merge($GLOBALS['aw_translations'], $translations);
        }
    }
}

/**
 * Get translation by key (supports dot notation)
 * @param string $key Translation key (e.g., 'nav.home', 'footer.contact')
 * @param string $default Default value if key not found
 * @return string Translated text or default/key
 */
function t($key, $default = null) {
    $parts = explode('.', $key);
    $value = $GLOBALS['aw_translations'];

    foreach ($parts as $part) {
        if (is_array($value) && isset($value[$part])) {
            $value = $value[$part];
        } else {
            // Key not found, return default or key itself
            return $default !== null ? $default : $key;
        }
    }

    return is_string($value) ? $value : ($default !== null ? $default : $key);
}

// Auto-load shared translations when this file is included
load_translations();
