<?php
// Determine base paths based on current directory
$inSubfolder = (strpos($_SERVER['REQUEST_URI'], '/id/') !== false ||
                strpos($_SERVER['REQUEST_URI'], '/species/') !== false ||
                strpos($_SERVER['REQUEST_URI'], '/games/') !== false);
$base = $inSubfolder ? '../' : '';
$idPath = $inSubfolder ? '' : 'id/';
?>
<nav>
<input id="mandible-toggle" class="mandible" type="checkbox">
<label class="colony-sigil" for="mandible-toggle">
    <svg class="sigil-img" viewBox="0 0 95 58" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="blueGradNav" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#87CEEB"/>
                <stop offset="100%" stop-color="#2c5aa0"/>
            </linearGradient>
        </defs>
        <text x="3" y="42" font-size="52" font-weight="900" font-family="Inter, Arial, sans-serif"
              fill="white" stroke="url(#blueGradNav)" stroke-width="3" paint-order="stroke fill">A</text>
        <text x="25" y="42" font-size="52" font-weight="900" font-family="Inter, Arial, sans-serif"
              fill="black" stroke="url(#blueGradNav)" stroke-width="3" paint-order="stroke fill">W</text>
        <text x="0" y="54" font-size="11" font-family="Inter, Arial, sans-serif" class="sigil-domain"
              text-anchor="start" letter-spacing="1">antworld.org</text>
    </svg>
    <span class="scape">▼</span>
</label>
<ul class="trail">
<li class="worker"><a href="<?php echo $base; ?>index.html">
	<span class="icon icon-home"></span><span class="scent">Home</span></a></li>
<li class="worker"><a href="<?php echo $base.$idPath; ?>confirmed.ergate_id.html">
	<span class="icon icon-bug"></span><span class="scent">Start ID</span></a></li>
<li class="worker"><a href="<?php echo $base; ?>morpho.html" title="Ant morphology guide">
	<span class="icon icon-morpho"></span><span class="scent">Morpho</span></a></li>
<li class="worker forager"><a href="#" title="Data">
	<span class="icon icon-stats-dots"></span><span class="scent">Data</span></a>
	<ul class="gallery">
		<li><a href="<?php echo $base; ?>geo_diversity.html"><span class="icon icon-stats-bars"></span> Geo-diversity</a></li>
		<li><a href="<?php echo $base; ?>tax_diversity.html"><span class="icon icon-pie-chart"></span> Taxo-diversity</a></li>
		<li><a href="<?php echo $base; ?>list_species.html"><span class="icon icon-menu2"></span> Species list</a></li>
	</ul></li>
<li class="worker"><a href="<?php echo $base; ?>Training.html" title="Train yourself to identify ants">
	<span class="icon icon-dice"></span><span class="scent">Training</span></a></li>
<li class="worker forager"><a href="#" title="Search for Subfamilies and Genera">
	<span class="icon icon-link"></span><span class="scent">Jump to</span></a>
	<ul class="gallery">
		<li class="category"><span class="icon icon-sort-amount-desc1"></span> Subfamilies</li>
		<li><a href="<?php echo $base.$idPath; ?>aenictinae_ergate.html">Aenictinae</a></li>
		<li><a href="<?php echo $base.$idPath; ?>amblyoponinae_ergate.html">Amblyoponinae</a></li>
		<li><a href="<?php echo $base.$idPath; ?>cerapachys&leptogenys_ergate.html">Cerapachyini</a></li>
		<li><a href="#" class="disabled">Dorylinae</a></li>
		<li><a href="<?php echo $base.$idPath; ?>formicinae_ergate.html">Formicinae</a></li>
		<li><a href="<?php echo $base.$idPath; ?>leptanillinae_ergate.html">Leptanillinae</a></li>
		<li><a href="<?php echo $base.$idPath; ?>palm_ergate_id.html">Myrmicinae</a></li>
		<li><a href="<?php echo $base.$idPath; ?>ponerinae_ergate.html">Ponerinae</a></li>
		<li><a href="#" class="disabled">Proceratiinae</a></li>
		<li class="category"><span class="icon icon-sort-amount-desc1"></span> Genera</li>
		<li><a href="<?php echo $base.$idPath; ?>acropyga_ergate.html">Acropyga</a></li>
		<li><a href="<?php echo $base.$idPath; ?>aenictinae_ergate.html">Aenictus</a></li>
		<li><a href="<?php echo $base.$idPath; ?>amblyoponinae_ergate.html">Amblyopone</a></li>
		<li><a href="<?php echo $base.$idPath; ?>leptanillinae_ergate.html">Anomalomyrma</a></li>
		<li><a href="<?php echo $base.$idPath; ?>lasiini_ergate.html">Anoplolepis</a></li>
		<li><a href="<?php echo $base.$idPath; ?>camponotini_ergate.html">Camponotus</a></li>
		<li><a href="<?php echo $base.$idPath; ?>cerapachys_ergate.html">Cerapachys</a></li>
		<li><a href="#" class="disabled">Dorylus</a></li>
		<li><a href="<?php echo $base.$idPath; ?>lasius_ergate.html">Lasius</a></li>
		<li><a href="<?php echo $base.$idPath; ?>leptanilla_ergate.html">Leptanilla</a></li>
		<li><a href="<?php echo $base.$idPath; ?>littleformicinae_ergate.html">Plagiolepis</a></li>
		<li><a href="<?php echo $base.$idPath; ?>polyergus_ergate.html">Polyergus</a></li>
		<li><a href="<?php echo $base.$idPath; ?>camponotini_ergate.html">Polyrhachis</a></li>
		<li><a href="#" class="disabled">Ponera</a></li>
		<li><a href="<?php echo $base.$idPath; ?>lasiini_ergate.html">Prenolepis</a></li>
		<li><a href="#" class="disabled">Proceratium</a></li>
		<li><a href="<?php echo $base.$idPath; ?>leptanillinae_ergate.html">Protanilla</a></li>
	</ul></li>
<li class="worker"><a href="<?php echo $base; ?>sources.html" title="Sources">
	<span class="icon icon-books"></span><span class="scent">Sources</span></a></li>
<li class="worker">
	<button class="theme-toggle" id="themeToggle" title="Toggle light/dark mode" aria-label="Toggle theme">
		<span class="theme-icon theme-icon-moon"></span>
		<span class="theme-switch"></span>
		<span class="theme-icon theme-icon-sun"></span>
	</button>
</li>
</ul>
</nav>
<script>
// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.addEventListener('click', function() {
            var html = document.documentElement;
            var isLight = html.classList.toggle('light-mode');
            localStorage.setItem('aw-theme', isLight ? 'light' : 'dark');
        });
    }
});
</script>
