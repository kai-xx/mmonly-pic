<?php
//定时生成网站地图
require_once(dirname(__FILE__).'/include/common.inc.php');
include(DEDEINC."/arc.listview.class.php");
$lv = new ListView();
//解析模板到字符串
$lv->PartView = new PartView($lv->TypeID,false);
$lv->PartView->SetTypeLink($lv->TypeLink);
$lv->PartView->SetTemplet(DEDETEMPLATE.'/default/sitemap.xml');
$html = $lv->PartView->GetResult();
file_put_contents('./sitemap.xml',$html);
?>