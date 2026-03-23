<?php include_once("../php/international.php"); ?>
<meta charset="utf-8"/><meta http-equiv="language" content="english, en">
<meta name="author" content="AntWorld.org">
<link rel="stylesheet" href="../css/css_antworld.css"/>
<link rel="stylesheet" href="../css/antworld-icons.css"/>
<!-- Page-specific description should be in the HTML file -->
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Theme Toggle Script - load early to prevent flash -->
<script>
(function() {
    var savedTheme = localStorage.getItem('aw-theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (savedTheme === 'light' || (!savedTheme && !prefersDark)) {
        document.documentElement.classList.add('light-mode');
    }
})();
</script>
<?php include("../php/favicon.php"); ?><?php include("../php/scripts.php") ?>
