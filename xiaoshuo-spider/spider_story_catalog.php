<?php
/**
 * @version        $Id: story_catalog.php 1 9:02 2010年9月25日Z 蓝色随想 $
 * @package        DedeCMS.Module.Book
 * @copyright      Copyright (c) 2007 - 2010, DesDev, Inc.
 * @license        http://help.dedecms.com/usersguide/license.html
 * @link           http://www.dedecms.com
 */

require_once(dirname(__FILE__). "/config_html.php");
if(!isset($action)) $action = '';

if(!isset($stypes)) $stypes = '';

//  action:add,
//  classname:武侠小说,
//  pid:0,
//  rank:0,
//  booktype:0,
//  keywords:武侠,
//  description:金庸,
//  Submit:增加栏目
//增加栏目
/*
function SaveNew();
*/

if($action=='add')
{
    $inQuery = "INSERT INTO #@__story_catalog(classname,pid,rank,listrule,viewrule,booktype,keywords,description)
    VALUES('$classname','$pid','$rank','','','$booktype','$keywords','$description')";
    $rs = $dsql->ExecuteNoneQuery($inQuery);
    if($rs)
    {
        $arcID = $dsql->GetLastID();
        exit(json_encode([
            'id' => $arcID
        ]));
    }
}
