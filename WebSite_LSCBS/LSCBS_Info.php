<?php
	header("Content-type: text/html; charset=utf-8");
    $params = $_POST["LID"];
    #$params = $_POST["title"];
	$path="STBERT_Cilent2.py ";
	$python = $path.$params;
	#echo $python;
	#$command = escapeshellcmd($python);
	#$output = shell_exec($python);
	#$output = shell_exec($command);
	#$output = shell_exec($python);
	#$output = exec($python);
	$output = passthru("py STBERT_Cilent2.py $params");
	#$output = shell_exec($path."\"".$params."\"");
	#$output = exec($path."\"".$params."\"");
	echo $output;
	
?>

