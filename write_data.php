<?php
header('Access-Control-Allow-Origin: *.scripts.mit.edu/*');
// get the filename and filedata from the POST message
$post_data = json_decode(file_get_contents('php://input'), true);
$data = $post_data['filedata'];
$name = $post_data['filename']; 
// write the file to disk
file_put_contents($name, $data);
?>
