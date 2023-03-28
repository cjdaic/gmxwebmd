<?php
// 从POST请求中获取json数据
$json_data = file_get_contents("php://input");
// 检查json数据是否有效
if (strlen($json_data) > 0 && isValidJSON($json_data)) {
  // 将json数据转换为数组
  $data = json_decode($json_data, true);
  // 获取id和value
  $id = $data['id'];
  $value = $data['value'];
  // 打开或创建mydata.json文件
  $file = fopen("mydata.json", "w");
  // 检查文件是否可写
  if (is_writable($file)) {
    // 将id和value写入文件
    fwrite($file, "$id: $value\n");
    // 关闭文件
    fclose($file);
    // 返回成功信息
    echo "Success";
  } else {
    // 返回错误信息
    echo "Error: file is not writable";
  }
} else {
  // 返回错误信息
  echo "Error: invalid json data";
}
// 定义一个函数，用于检查json数据是否有效
function isValidJSON($str) {
   json_decode($str);
   return json_last_error() == JSON_ERROR_NONE;
}
?>