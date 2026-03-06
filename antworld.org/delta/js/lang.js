/**
 * AntWorld Language Toggle Handler
 */
(function() {
    'use strict';


    function getCurrentLang() {
        var match = document.cookie.match(/aw_lang=([^;]+)/);
        return match ? match[1] : 'en';
    }


    function getPhpPath() {
        var path = window.location.pathname;
        if (path.indexOf('/id/species/') !== -1) {
            return '../../php/';
        } else if (path.indexOf('/id/') !== -1 || path.indexOf('/games/') !== -1) {
            return '../php/';
        }
        return 'php/';
    }


    function setLanguage(lang) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', getPhpPath() + 'lang-handler.php', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {

                window.location.reload();
            }
        };
        xhr.send(JSON.stringify({ lang: lang }));
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
