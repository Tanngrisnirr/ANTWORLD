/**
 * AntWorld Language Toggle Handler
 * Works fully client-side for offline support
 */
(function() {
    'use strict';

    function getCurrentLang() {
        var match = document.cookie.match(/aw_lang=([^;]+)/);
        return match ? match[1] : 'en';
    }

    // Set cookie client-side (works offline)
    function setLanguage(lang) {
        // Set cookie for 1 year
        var expires = new Date();
        expires.setFullYear(expires.getFullYear() + 1);
        document.cookie = 'aw_lang=' + lang + ';expires=' + expires.toUTCString() + ';path=/;SameSite=Lax';

        // Reload to apply language
        window.location.reload();
    }

    function toggleLanguage() {
        var current = getCurrentLang();
        var next = (current === 'en') ? 'fr' : 'en';
        setLanguage(next);
    }

    function init() {
        var btn = document.getElementById('langToggleNav');
        if (btn) {
            var langText = btn.querySelector('.lang-text');
            if (langText) {
                langText.textContent = getCurrentLang().toUpperCase();
            }

            btn.addEventListener('click', function(e) {
                e.preventDefault();
                toggleLanguage();
            });
        }

        // Apply language to elements with data-en/data-fr attributes
        var lang = getCurrentLang();
        document.querySelectorAll('[data-en][data-fr]:not(.def-item):not(.def-section-title)').forEach(function(el) {
            var text = el.getAttribute('data-' + lang);
            if (text) {
                el.textContent = text;
            }
        });

        document.querySelectorAll('.def-item[data-en][data-fr]').forEach(function(el) {
            var defText = el.querySelector('.def-text');
            if (defText) {
                defText.textContent = el.getAttribute('data-' + lang);
            }
        });

        document.querySelectorAll('.def-section-title[data-en][data-fr]').forEach(function(el) {
            el.textContent = el.getAttribute('data-' + lang);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
