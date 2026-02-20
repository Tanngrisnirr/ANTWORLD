<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta http-equiv="language" content="english, en">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Open source fonts: Inter (primary), with Arial as fallback -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
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
<?php include("php/header.html"); ?><?php include("php/nav.php"); ?><?php include("php/favicon.php"); ?><?php include("php/scripts.php") ?>