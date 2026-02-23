/**
 * AntWorld Language Toggle Handler
 */
(function() {
    'use strict';

    // Get current language from cookie
    function getCurrentLang() {
        var match = document.cookie.match(/aw_lang=([^;]+)/);
        return match ? match[1] : 'en';
    }

    // Determine PHP path based on current URL depth
    function getPhpPath() {
        var path = window.location.pathname;
        if (path.indexOf('/id/species/') !== -1) {
            return '../../php/';
        } else if (path.indexOf('/id/') !== -1 || path.indexOf('/games/') !== -1) {
            return '../php/';
        }
        return 'php/';
    }

    // Set language via AJAX and reload
    function setLanguage(lang) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', getPhpPath() + 'lang-handler.php', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                // Reload regardless of response - cookie may be set
                window.location.reload();
            }
        };
        xhr.send(JSON.stringify({ lang: lang }));
    }

    // Toggle between languages
    function toggleLanguage() {
        var current = getCurrentLang();
        var next = (current === 'en') ? 'fr' : 'en';
        setLanguage(next);
    }

    // Initialize when DOM is ready
    function init() {
        var btn = document.getElementById('langToggleNav');
        if (btn) {
            // Update button text to show current language
            var langText = btn.querySelector('.lang-text');
            if (langText) {
                langText.textContent = getCurrentLang().toUpperCase();
            }

            // Add click handler
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                toggleLanguage();
            });
        }

        // Handle elements with data-en/data-fr attributes (for morpho, SVGs, etc.)
        var lang = getCurrentLang();
        document.querySelectorAll('[data-en][data-fr]').forEach(function(el) {
            var text = el.getAttribute('data-' + lang);
            if (text) {
                el.textContent = text;
            }
        });
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
