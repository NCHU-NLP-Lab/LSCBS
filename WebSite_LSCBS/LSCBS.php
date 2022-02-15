<?php
	header("Content-type: text/html; charset=utf-8");
	$locale='en_US.UTF-8';
	putenv('LC_ALL='.$locale);
    $params = $_POST["title"];
    #$params = $_POST["title"];
	$path="STBERT_Cilent.py ";
	$python = $path.$params;
	#echo $python;
	#$command = escapeshellcmd($python);
	#$output = shell_exec($python);
	#$output = shell_exec($command);
	#$output = shell_exec($python);
	#$output = exec($python);
	$output = passthru("python STBERT_Cilent.py $params");
	#$output = shell_exec($path."\"".$params."\"");
	#$output = exec($path."\"".$params."\"");
	echo $output;
	
?>

