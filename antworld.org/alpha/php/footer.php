<?php
// Determine base path based on current directory depth
$basePath = '';
if (strpos($_SERVER['REQUEST_URI'], '/id/') !== false ||
    strpos($_SERVER['REQUEST_URI'], '/species/') !== false ||
    strpos($_SERVER['REQUEST_URI'], '/games/') !== false) {
    $basePath = '../';
}
?>
<footer class="aw-footer">
<a rel="license" href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank"><img alt="CC BY-NC 4.0" style="border:0; height:15px; vertical-align:middle;" src="https://licensebuttons.net/l/by-nc/4.0/80x15.png" /></a>
<span class="sep">|</span>
<a href="mailto:info@antworld.org">Contact</a>
<span class="sep">|</span>
<a href="<?php echo $basePath; ?>privacy.html">Privacy</a>
<span class="sep">|</span>
<a href="<?php echo $basePath; ?>credits.html">Credits</a>
<span class="sep">|</span>
<span class="last-updated">Updated <?php echo date('M Y'); ?></span>
</footer>
