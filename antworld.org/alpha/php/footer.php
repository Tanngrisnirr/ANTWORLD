<?php
// Determine base path based on current directory depth
$basePath = '';
if (strpos($_SERVER['REQUEST_URI'], '/id/species/') !== false) {
    $basePath = '../../';
} elseif (strpos($_SERVER['REQUEST_URI'], '/id/') !== false ||
    strpos($_SERVER['REQUEST_URI'], '/species/') !== false ||
    strpos($_SERVER['REQUEST_URI'], '/games/') !== false) {
    $basePath = '../';
}
?>
<footer class="aw-footer">
<a rel="license" href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank"><img alt="CC BY-NC 4.0" style="border:0; height:15px; vertical-align:middle;" src="<?php echo $basePath; ?>img/logos/cc-by-nc-4.0.png" /></a>
<span class="sep">|</span>
<a href="mailto:info@antworld.org"><?= t('footer.contact') ?></a>
<span class="sep">|</span>
<a href="<?php echo $basePath; ?>privacy.html"><?= t('footer.privacy') ?></a>
<span class="sep">|</span>
<a href="https://github.com/Tanngrisnirr/ANTWORLD" target="_blank"><?= t('footer.credits') ?></a>
<span class="sep">|</span>
<span class="last-updated"><?= t('footer.updated') ?> <?php
$lang = get_current_lang();
if ($lang === 'fr') {
    $mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
    echo date('j') . ' ' . $mois[date('n') - 1] . ' ' . date('Y');
} else {
    echo date('j F Y');
}
?></span>
</footer>
