<?php
/**
 * AntWorld SEO Configuration
 * Centralized SEO data for all pages
 */

// Site-wide defaults
$GLOBALS['aw_seo_defaults'] = [
    'site_name' => 'AntWorld.org',
    'site_url' => 'https://antworld.org',
    'default_image' => '/img/og-default.jpg',
    'locale' => 'en_US',
    'locale_alternate' => 'fr_FR',
    'twitter_card' => 'summary_large_image',
    'license' => 'https://creativecommons.org/licenses/by-nc/4.0/'
];

// Page-specific SEO configuration
// Keys are the page path without .html extension
$GLOBALS['aw_seo_pages'] = [
    'index' => [
        'title' => 'AntWorld.org | Ants of the Palearctic',
        'description' => 'Interactive identification key for the ants of the Palearctic region. Explore ant diversity, taxonomy, and distribution.',
        'type' => 'website',
        'schema_type' => 'WebSite'
    ],
    'morpho' => [
        'title' => 'Ant Morphology - Interactive Anatomy Guide',
        'description' => 'Interactive anatomical diagrams and morphometric definitions for ant identification. Explore head, mesosoma, and metasoma features.',
        'type' => 'article',
        'image' => '/img/og-morpho.jpg',
        'schema_type' => 'Article'
    ],
    'list_species' => [
        'title' => 'Palearctic Ant Species Checklist',
        'description' => 'Complete checklist of 936 ant species across 74 genera found in the Palearctic region. Browse by subfamily, genus, or search by name.',
        'type' => 'article',
        'schema_type' => 'Dataset'
    ],
    'geo_diversity' => [
        'title' => 'Geographic Distribution of Palearctic Ants',
        'description' => 'Interactive map and charts showing the geographic distribution of ant species across Palearctic regions including Europe, North Africa, and Asia.',
        'type' => 'article',
        'schema_type' => 'Dataset'
    ],
    'tax_diversity' => [
        'title' => 'Taxonomic Diversity of Palearctic Ants',
        'description' => 'Explore the taxonomic diversity of Palearctic ants with interactive charts showing species distribution across subfamilies, genera, and tribes.',
        'type' => 'article',
        'schema_type' => 'Dataset'
    ],
    'sources' => [
        'title' => 'Bibliography & References',
        'description' => 'Searchable bibliography of scientific literature and references used in AntWorld identification keys. Includes links to original publications.',
        'type' => 'article',
        'schema_type' => 'Article'
    ],
    'training' => [
        'title' => 'Ant Identification Training',
        'description' => 'Interactive training modules to improve your ant identification skills. Practice recognizing morphological features and taxonomic characteristics.',
        'type' => 'article',
        'schema_type' => 'Article'
    ],
    'credits' => [
        'title' => 'Credits & Acknowledgments',
        'description' => 'Credits, image attributions, and acknowledgments for contributors to the AntWorld identification system.',
        'type' => 'article',
        'schema_type' => 'Article'
    ],
    'privacy' => [
        'title' => 'Privacy Policy',
        'description' => 'Privacy policy for AntWorld.org. We respect your privacy and collect minimal data.',
        'type' => 'article',
        'schema_type' => 'Article'
    ],
    // ID keys - default config for identification pages
    'id/confirmed.ergate_id' => [
        'title' => 'Ant Identification Key - Start Here',
        'description' => 'Begin identifying worker ants of the Palearctic region with this interactive dichotomous key.',
        'type' => 'article',
        'schema_type' => 'Article'
    ]
];

/**
 * Get current page identifier from URL
 */
function aw_get_page_id() {
    $path = $_SERVER['PHP_SELF'] ?? $_SERVER['SCRIPT_NAME'] ?? '';

    // Remove leading slash and .html extension
    $page = ltrim($path, '/');
    $page = preg_replace('/\.html?$/i', '', $page);

    // Remove dev/staging prefixes (alpha/, beta/, delta/)
    $page = preg_replace('/^(alpha|beta|delta)\//', '', $page);

    // Handle index pages
    if (empty($page) || $page === 'index') {
        return 'index';
    }

    return $page;
}

/**
 * Get canonical URL for current page
 */
function aw_get_canonical_url() {
    $defaults = $GLOBALS['aw_seo_defaults'];
    $page = aw_get_page_id();

    if ($page === 'index') {
        return $defaults['site_url'] . '/';
    }

    return $defaults['site_url'] . '/' . $page;
}

/**
 * Get SEO config for current page
 */
function aw_get_seo_config() {
    $page = aw_get_page_id();
    $defaults = $GLOBALS['aw_seo_defaults'];
    $pages = $GLOBALS['aw_seo_pages'];

    // Check for exact match
    if (isset($pages[$page])) {
        return array_merge($defaults, $pages[$page]);
    }

    // Check for ID key pages (fallback pattern)
    if (strpos($page, 'id/') === 0) {
        $idConfig = [
            'title' => 'Ant Identification Key',
            'description' => 'Interactive dichotomous key for identifying Palearctic ants.',
            'type' => 'article',
            'schema_type' => 'Article'
        ];
        return array_merge($defaults, $idConfig);
    }

    // Default fallback
    return array_merge($defaults, [
        'title' => 'AntWorld.org',
        'description' => 'Interactive identification keys for Palearctic ants.',
        'type' => 'website',
        'schema_type' => 'WebPage'
    ]);
}

/**
 * Output canonical link tag (only once per page)
 */
function aw_output_canonical() {
    // Prevent duplicate canonical tags
    if (defined('AW_CANONICAL_OUTPUT')) {
        return;
    }
    define('AW_CANONICAL_OUTPUT', true);

    $url = aw_get_canonical_url();
    echo '<link rel="canonical" href="' . htmlspecialchars($url) . '">' . "\n";
}

/**
 * Output hreflang tags
 * Since language is cookie-based (same URL serves all languages),
 * we use x-default pointing to the same URL
 */
function aw_output_hreflang() {
    $url = aw_get_canonical_url();
    echo '<link rel="alternate" hreflang="en" href="' . htmlspecialchars($url) . '">' . "\n";
    echo '<link rel="alternate" hreflang="fr" href="' . htmlspecialchars($url) . '">' . "\n";
    echo '<link rel="alternate" hreflang="x-default" href="' . htmlspecialchars($url) . '">' . "\n";
}

/**
 * Output Open Graph meta tags
 */
function aw_output_opengraph() {
    $config = aw_get_seo_config();
    $url = aw_get_canonical_url();
    $image = $config['site_url'] . ($config['image'] ?? $config['default_image']);

    echo '<meta property="og:type" content="' . htmlspecialchars($config['type'] ?? 'website') . '">' . "\n";
    echo '<meta property="og:site_name" content="' . htmlspecialchars($config['site_name']) . '">' . "\n";
    echo '<meta property="og:title" content="' . htmlspecialchars($config['title']) . '">' . "\n";
    echo '<meta property="og:description" content="' . htmlspecialchars($config['description']) . '">' . "\n";
    echo '<meta property="og:url" content="' . htmlspecialchars($url) . '">' . "\n";
    echo '<meta property="og:image" content="' . htmlspecialchars($image) . '">' . "\n";
    echo '<meta property="og:locale" content="' . htmlspecialchars($config['locale']) . '">' . "\n";
    echo '<meta property="og:locale:alternate" content="' . htmlspecialchars($config['locale_alternate']) . '">' . "\n";
}

/**
 * Output Twitter Card meta tags
 */
function aw_output_twitter() {
    $config = aw_get_seo_config();
    $image = $config['site_url'] . ($config['image'] ?? $config['default_image']);

    echo '<meta name="twitter:card" content="' . htmlspecialchars($config['twitter_card']) . '">' . "\n";
    echo '<meta name="twitter:title" content="' . htmlspecialchars($config['title']) . '">' . "\n";
    echo '<meta name="twitter:description" content="' . htmlspecialchars($config['description']) . '">' . "\n";
    echo '<meta name="twitter:image" content="' . htmlspecialchars($image) . '">' . "\n";
}

/**
 * Output JSON-LD structured data
 */
function aw_output_jsonld() {
    $config = aw_get_seo_config();
    $url = aw_get_canonical_url();
    $page = aw_get_page_id();

    // Base graph with WebSite and Organization
    $graph = [];

    // Always include WebSite schema
    $graph[] = [
        '@type' => 'WebSite',
        '@id' => $config['site_url'] . '/#website',
        'name' => $config['site_name'],
        'url' => $config['site_url'],
        'description' => 'Interactive identification keys for Palearctic ants',
        'inLanguage' => ['en', 'fr'],
        'publisher' => ['@id' => $config['site_url'] . '/#organization']
    ];

    // Always include Organization schema
    $graph[] = [
        '@type' => 'Organization',
        '@id' => $config['site_url'] . '/#organization',
        'name' => 'AntWorld',
        'url' => $config['site_url'],
        'logo' => [
            '@type' => 'ImageObject',
            'url' => $config['site_url'] . '/img/logo.png'
        ]
    ];

    // Page-specific schema
    $schemaType = $config['schema_type'] ?? 'WebPage';

    if ($schemaType === 'Dataset') {
        $graph[] = [
            '@type' => 'Dataset',
            'name' => $config['title'],
            'description' => $config['description'],
            'url' => $url,
            'license' => $config['license'],
            'creator' => ['@id' => $config['site_url'] . '/#organization'],
            'inLanguage' => ['en', 'fr'],
            'spatialCoverage' => [
                '@type' => 'Place',
                'name' => 'Palearctic region'
            ]
        ];
    } elseif ($schemaType === 'Article') {
        $graph[] = [
            '@type' => 'Article',
            'headline' => $config['title'],
            'description' => $config['description'],
            'url' => $url,
            'inLanguage' => ['en', 'fr'],
            'author' => ['@id' => $config['site_url'] . '/#organization'],
            'publisher' => ['@id' => $config['site_url'] . '/#organization'],
            'mainEntityOfPage' => $url
        ];
    }

    // Build final JSON-LD
    $jsonld = [
        '@context' => 'https://schema.org',
        '@graph' => $graph
    ];

    echo '<script type="application/ld+json">' . "\n";
    echo json_encode($jsonld, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    echo "\n</script>\n";
}

/**
 * Output standard meta description tag
 */
function aw_output_description() {
    $config = aw_get_seo_config();
    echo '<meta name="description" content="' . htmlspecialchars($config['description']) . '">' . "\n";
}

/**
 * Output all SEO tags
 */
function aw_output_seo() {
    echo "<!-- SEO Tags -->\n";
    aw_output_description();
    aw_output_canonical();
    aw_output_hreflang();
    echo "<!-- Open Graph -->\n";
    aw_output_opengraph();
    echo "<!-- Twitter Card -->\n";
    aw_output_twitter();
    echo "<!-- Structured Data -->\n";
    aw_output_jsonld();
}
