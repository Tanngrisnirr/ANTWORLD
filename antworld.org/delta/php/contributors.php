<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
		        <!--[if lt IE 9]>
                <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
                <![endif]-->
<meta http-equiv="language" content="english, en">
<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
<link rel="stylesheet" type="text/css" href="../css/antworld.css" media="screen"/>
        <title>Palearctic Ant Key</title>
		    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/jquery-ui.min.js"></script>
	<script type="text/javascript">
 $(document).ready(function(){
 $(".en").hide();
 $(".en").fadeIn(1000, "swing");
        $(".fr").hide();
 $("#francais").click(function(){
        $(".en").hide();
        $(".fr").fadeIn(2000, "swing");
 });
 $("#english").click(function(){
        $(".en").fadeIn(2000, "swing");
 $(".fr").fadeOut();
 });
 	});
	</script>
		<script src="mobile/fastclick/lib/fastclick.js" type="text/javascript">
		window.addEventListener('load', function() {
		new FastClick(document.body);}, false);</script>
<script src="../js/jquery_1_11_3_jquery_min.js"></script>
<script>
$(document).ready(function(){
		$(".group1").hide();
		$(".group2").hide();
		$(".group3").hide();
		$(".group4").hide();
    $("#grp1").click(function(){
        $(".group1").slideToggle("slow");
    });
	$("#grp2").click(function(){
        $(".group2").slideToggle("slow");
    });
    $("#grp3").click(function(){
		$(".group4").slideUp("fast");
        $(".group3").slideToggle("slow");
    });
    $("#grp4").click(function(){
		$(".group3").slideUp("fast");
        $(".group4").slideToggle("slow");
    });
});
</script>
    </head>  
    <body><header><h1>Ants of the Palearctic <em>version September 2015</em></h1></header>
<?php include("navigation_contributors.php"); ?>
<article>
</br>
<?php
    if (isset($_POST['speudo']) AND $_POST['speudo'] ==  "contributor" && isset($_POST['mot_de_passe']) AND $_POST['mot_de_passe'] ==  "&45141%") // Si le mot de passe est bon
    {
    ?>
<?php include("php/top.php"); ?>
<img id="english" src="../img/uk-us_flag_40x40.png" title="English"/>
<img id="francais" src="../img/drapeau_francais_40x40.jpg" title="En Francais"/>
<span class="en"><h2>How to contribute</h2>
<p>
Once done, don't forget to log out !
</p>
</span>
<span class="fr"><h2 class="h2one">Comment contribuer ?</h2>
<p4>
<span class="red">Une fois terminé, n'oublier pas de vous déconnecter ! </span>
<?php include("sent.php"); ?>
<h3 id="grp3">Signaler ou poster une idée <span class="icon icon-sort-amount-desc"></span></h3>
<div class="group3">
<p4>
Pour signaler;</br>
- Une erreur d'affichage cliquez sur<a href="contributions/" style="height:24px; line-height:24px;" title="Ajouter impression d'écran" alt="Ajouter impression d'écran"><span class="icon icon-blocked"> Erreur d'affichage</span>.</a></br>
- Une faute d'orthographe ou de syntaxe, une question, une idée  cliquez ici<a href="mailto:contact@palearcticantkey.eu?subject=faute_de_langue" style="height:24px; line-height:24px;" title="Envoyer par mail" alt="Envoyer par mail"><span class="icon icon-cross"> Erreur de langue</span></a>.</br>
- Une question, une idée cliquez ici<a href="mailto:contact@palearcticantkey.eu?subject=question/idee" style="height:24px; line-height:24px;" title="Envoyer par mail" alt="Envoyer par mail"><span class="icon icon-cross"> Question/idée</span></a>.</br>
</p4>
</div>
<h3 id="grp4">Ajouter du contenu <span class="icon icon-sort-amount-desc"></span></h3>
<div class="group4">
<p4>
Pour ajouter:</br>
- un document écrit (pdf ou autre)</br>
- une vidéo (tout format, de qualité relativement bonne)</br>
- une image(tout format, de qualité relativement bonne)</br>
</p4>
<form action="sent.php" method="post" enctype="multipart/form-data">
        <p4>
                Formulaire d'envoi de fichier :
                <input type="file" name="monfichier" />
                <input type="submit" value="Envoyer le fichier" />
        </p4>
</form>
</div>
<p4>
</br><span class="red">/!\ Avant d'ajouter un fichier regardez <a href="../upload/" target="blank" title="upload" alt="upload"><b>ici</b></a> s'il n'existe pas déjà dans le dossier /!\</span></br>
</span>
</p4>
    <?php
    }
    else // Sinon, on affiche un message d'erreur
    {echo 'Mot de passe et/ou speudo incorrect(s)';}
?>
</article>
<?php include("footer_contributors.php"); ?>
    </body>
</html>