dede小说模块 详情页面空白问题
打开story.php文件找到 

require_once(dirname(__FILE__).'./include/story.view.class.php'); 

将那个点去掉改后就是下面这样 

require_once(dirname(__FILE__).'/include/story.view.class.php'); 

同样的小说频道的分类打不开也是一样 

打开list.php文件找到 

require_once(dirname(__FILE__).'./include/story.view.class.php'); 

修改为 

require_once(dirname(__FILE__).'/include/story.view.class.php');