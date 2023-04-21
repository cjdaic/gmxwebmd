<?php
// 从POST请求中获取json数据
$json_data = file_get_contents("php://input");
// 检查json数据是否有效
if (strlen($json_data) > 0 && json_decode($json_data) != null) {
  // 将json数据转换为数组
  $data = json_decode($json_data, true);
  // 获取id和value
  $id = $data['id'];
  $value = $data['value'];
  // 打开或创建mydata.json文件
 
  // 检查文件是否可写
  if (is_writable("usr/usr.json")) {
    // 将id和value写入文件

    $content = file_get_contents("usr/usr.json");
    $array = json_decode($content,true);
    $array[$id] = $value; 
    $content = json_encode($array);
    // 关闭文件
    file_put_contents("usr/usr.json", $content);

    echo "Success";
  } else {
    // 返回错误信息
    echo "Error: file is not writable";
  }
} else {
  echo "nmsl";
}

?>