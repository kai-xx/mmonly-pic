<?php
/**
 * Created by PhpStorm.
 * User: carter
 * Date: 2018-12-06
 * Time: 21:25
 */

//archives_do.php?aid=484&dopost=viewArchives
require_once(dirname(__FILE__).'/config_html.php');
require_once(DEDEADMIN.'/inc/inc_batchup.php');
require_once(DEDEADMIN.'/inc/inc_archives_functions.php');
require_once(DEDEINC.'/typelink.class.php');
require_once(DEDEINC.'/arc.archives.class.php');
$ENV_GOBACK_URL = (empty($_COOKIE['ENV_GOBACK_URL']) ? 'content_list.php' : $_COOKIE['ENV_GOBACK_URL']);

$aid = isset($aid) ? preg_replace("#[^0-9]#", '', $aid) : '';

if (!is_numeric($aid)) exit();
if ($aid <= 0) exit();
$aid = preg_replace("#[^0-9]#", '', $aid);

//获取主表信息
$query = "SELECT arc.*,ch.maintable,ch.addtable,ch.issystem,ch.editcon,
              tp.typedir,tp.typename,tp.corank,tp.namerule,tp.namerule2,tp.ispart,tp.moresite,tp.sitepath,tp.siteurl
           FROM `#@__arctiny` arc
           LEFT JOIN `#@__arctype` tp ON tp.id=arc.typeid
           LEFT JOIN `#@__channeltype` ch ON ch.id=tp.channeltype
           WHERE arc.id='$aid' ";
$trow = $dsql->GetOne($query);
$trow['maintable'] = ( trim($trow['maintable'])=='' ? '#@__archives' : trim($trow['maintable']) );
if($trow['issystem'] != -1)
{
    $arcQuery = "SELECT arc.*,tp.typedir,tp.typename,tp.corank,tp.namerule,tp.namerule2,tp.ispart,tp.moresite,tp.sitepath,tp.siteurl
                   FROM `{$trow['maintable']}` arc LEFT JOIN `#@__arctype` tp on arc.typeid=tp.id
                   LEFT JOIN `#@__channeltype` ch on ch.id=arc.channel WHERE arc.id='$aid' ";
    $arcRow = $dsql->GetOne($arcQuery);
    PutCookie('DedeUserID',$arcRow['mid'],1800);
    PutCookie('DedeLoginTime',time(),1800);
    if($arcRow['ismake']==-1 || $arcRow['corank']!=0 || $arcRow['arcrank']!=0 || ($arcRow['typeid']==0 && $arcRow['channel']!=-1) || $arcRow['money']>0)
    {
        echo "<script language='javascript'>location.href='{$cfg_phpurl}/view.php?aid={$aid}';</script>";
        exit();
    }
}
else
{
    $arcRow['id'] = $aid;
    $arcRow['typeid'] = $trow['typeid'];
    $arcRow['senddate'] = $trow['senddate'];
    $arcRow['title'] = '';
    $arcRow['ismake'] = 1;
    $arcRow['arcrank'] = $trow['corank'];
    $arcRow['namerule'] = $trow['namerule'];
    $arcRow['typedir'] = $trow['typedir'];
    $arcRow['money'] = 0;
    $arcRow['filename'] = '';
    $arcRow['moresite'] = $trow['moresite'];
    $arcRow['siteurl'] = $trow['siteurl'];
    $arcRow['sitepath'] = $trow['sitepath'];
}
$arcurl  = GetFileUrl($arcRow['id'],$arcRow['typeid'],$arcRow['senddate'],$arcRow['title'],$arcRow['ismake'],$arcRow['arcrank'],
    $arcRow['namerule'],$arcRow['typedir'],$arcRow['money'],$arcRow['filename'],$arcRow['moresite'],$arcRow['siteurl'],$arcRow['sitepath']);
$arcfile = GetFileUrl($arcRow['id'],$arcRow['typeid'],$arcRow['senddate'],$arcRow['title'],
    $arcRow['ismake'],$arcRow['arcrank'],$arcRow['namerule'],$arcRow['typedir'],$arcRow['money'],$arcRow['filename']);
if(preg_match("#^http:#", $arcfile))
{
    $arcfile = preg_replace("#^http:\/\/([^\/]*)\/#i", '/', $arcfile);
}
$truefile = GetTruePath().$arcfile;
if(!file_exists($truefile))
{
    MakeArt($aid,TRUE);
}
echo "<script language='javascript'>location.href='$arcurl"."?".time()."';</script>";
exit();