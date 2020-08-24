<?php
/**
* @param string $con 待解密内容
* @param string $key 密钥
* @return string
*/
ini_set ('memory_limit', '-1');

function decrypt($string, $key)
{
     $decrypted = openssl_decrypt($string, 'AES128', $key, OPENSSL_RAW_DATA); 
     return $decrypted;
}

$con = $argv[1];
$key = $argv[2];
$result= $argv[3];
 
$fcon = fopen($con, "rb");
$fkey = fopen($key, "rb");
$f = fopen($result, 'wb');
 
$file_con = fread($fcon, filesize($con));
$file_key = fread($fkey, filesize($key));
 
fwrite($f, decrypt($file_con, $file_key)); 
 
fclose($f);
fclose($fcon);
fclose($fkey);

?>
