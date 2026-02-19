<?php
// Testons si le fichier a bien été envoyé et s'il n'y a pas d'erreur
if (isset($_FILES['monfichier']) AND $_FILES['monfichier']['error'] == 0)
{
        // Testons si le fichier n'est pas trop gros
        if ($_FILES['monfichier']['size'] <= 10000000)
        {
                // Testons si l'extension est autorisée
                $infosfichier = pathinfo($_FILES['monfichier']['name']);
                $extension_upload = $infosfichier['extension'];
                $extensions_autorisees = array('jpg', 'jpeg', 'gif', 'png', 'pns', 'ico', 'otb', 'pcf', 'pcx', 'pdn', 'pgm', 'pict', 'pct', 'xcf', 'odf', 'sxm', 'bdf', 'otf', 'ttf', 'ttc', 'mm', 'tgz', 'rar', 'zip', 'wav', 'raw', 'flac', 'm4a', 'mp2', 'mp3', 'aac', 'mpeg', 'ogg', 'txt', 'log', 'asc', 'a', 'kdbx', 'kdb', 'pps', 'ppt', 'pdf', 'otp', 'ott', 'odt', 'odp', 'gdoc', 'dot', 'docx', 'docm', 'rtf');
                if (in_array($extension_upload, $extensions_autorisees))
                {
                        // On peut valider le fichier et le stocker définitivement
                        move_uploaded_file($_FILES['monfichier']['tmp_name'], '../upload/' . basename($_FILES['monfichier']['name']));
                        echo "L'envoi a bien été effectué !";
                }
        }
}

	/*if (file_exists($target_file))
	{
    echo "Sorry, file already exists.";
    $uploadOk = 0;
	}
		else
		{
		echo "To big or already exist!";	
		}*/

?>