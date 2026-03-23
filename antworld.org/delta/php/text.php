<?php
header ("Content-type: image/png");
$image = imagecreatefrompng("../img/placeholder_ant.png");

$orange = imagecolorallocate($image, 255, 128, 0);
$bleu = imagecolorallocate($image, 0, 0, 255);
$bleuclair = imagecolorallocate($image, 156, 227, 254);
$noir = imagecolorallocate($image, 0, 0, 0);
$blanc = imagecolorallocate($image, 255, 255, 255);

imagefilledellipse($image, 134, 134, 30, 30, $noir);
imagefilledellipse($image, 134, 134, 24, 24, $blanc);
imagesetthickness($image, 25); // thickness
ImageEllipse($image, 134, 134, 30, 30, $noir); // (image, x, y, largeur, hauteur, couleur)
imagestring($image, 55, 130, 127, "C", $noir); // (image, font-size, x, y, "text", couleur)

imagepng($image);
imagedestroy($im);
?>