生成静态页面方法

游戏

1 复制gamead/config.php 为gamead/config_html.php
```php
//注释掉
/*if($cuserLogin->getUserID()==-1)
{
    if ( preg_match("#PHP (.*) Development Server#",$_SERVER['SERVER_SOFTWARE']) )
    {
        $dirname = dirname($_SERVER['SCRIPT_NAME']);
        header("location:{$dirname}/login.php?gotopage=".urlencode($dedeNowurl));
    } else {
        header("location:login.php?gotopage=".urlencode($dedeNowurl));
    }
    exit();
}*/
```
2 复制gamead/archives_do.php只保留代码中viewArchives部分命名为html.php

图片


