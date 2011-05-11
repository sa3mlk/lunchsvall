<?php

$json_data = @file_get_contents("http://ssh.gulle.se/get_json.php");
$filename = @strftime("%Y-%m-%d.json", time());

// Save a local copy on the server
if (!file_exists($filename))
{
	@file_put_contents($filename, $json_data);
}

echo $json_data;

?>
