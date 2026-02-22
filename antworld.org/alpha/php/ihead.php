<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta http-equiv="language" content="english, en">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- System font stack - no external requests -->
<link rel="stylesheet" href="css/css_antworld.css" type="text/css">
<link rel="stylesheet" href="css/antworld-icons.css" type="text/css">
<!-- IE9 and below no longer supported (0% market share) -->
<!-- Theme Toggle Script - load early to prevent flash -->
<script>
(function() {
    // Check for saved theme preference or system preference
    var savedTheme = localStorage.getItem('aw-theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Apply theme immediately (before DOM loads) to prevent flash
    if (savedTheme === 'light' || (!savedTheme && !prefersDark)) {
        document.documentElement.classList.add('light-mode');
    }
})();
</script>
<?php include("php/nav.php"); ?><?php include("php/favicon.php"); ?><?php include("php/scripts.php") ?>