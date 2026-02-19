<?php
header ("Content-type: image/png"); // L'image que l'on va créer est un png
// On charge d'abord les images
$source = imagecreatefrompng("quote_image4.png"); // Le logo est la source
$destination = imagecreatefrompng("../img/techno_albipes.peprofil_mini.png"); // La photo est la destination
 //imagealphablending($source, true); Conserver ou non l'alpha-blending
 //imagesavealpha($source, true); Definir le drapeaux-blending
// Les fonctions imagesx et imagesy renvoient la largeur et la hauteur d'une image
$largeur_source = imagesx($source);
$hauteur_source = imagesy($source);
$largeur_destination = imagesx($destination);
$hauteur_destination = imagesy($destination);
// On veut placer le logo en bas à droite, on calcule les coordonnées où on doit placer le logo sur la photo
$destination_x = $largeur_destination - $largeur_source;
$destination_y =  $hauteur_destination - $hauteur_source;
// On met le logo (source) dans l'image de destination (la photo)
imagecopymerge($destination, $source, $destination_x, $destination_y, 0, 0, $largeur_source, $hauteur_source, 90); //le dernier nombre est l'opacité
// On affiche l'image de destination qui a été fusionnée avec le logo
imagepng($destination);
?>