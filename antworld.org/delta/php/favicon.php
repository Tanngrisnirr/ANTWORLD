<?php

$iconPath = 'icon/';
if (strpos($_SERVER['REQUEST_URI'], '/id/species/') !== false) {
    $iconPath = '../../icon/';
} elseif (strpos($_SERVER['REQUEST_URI'], '/id/') !== false) {
    $iconPath = '../icon/';
}
?>
<link rel="icon" type="image/x-icon" href="<?php echo $iconPath; ?>favicon.ico">
<link rel="icon" type="image/svg+xml" href="<?php echo $iconPath; ?>favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="<?php echo $iconPath; ?>favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="<?php echo $iconPath; ?>apple-touch-icon.png">
<link rel="manifest" href="<?php echo $iconPath; ?>manifest.json">
<meta name="theme-color" content="#0a0a1a">
