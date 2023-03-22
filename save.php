<?php
$data = json_decode(file_get_contents("php://input"), true);
$buttonValue = $data["buttonValue"];
$jsonData = array("buttonValue" => $buttonValue);
$jsonFile = fopen("mydata.json", "w") or die("Unable to open file!");
fwrite($jsonFile, json_encode($jsonData));
fclose($jsonFile);
echo "Data saved successfully!";
?>