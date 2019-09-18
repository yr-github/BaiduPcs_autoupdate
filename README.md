# BaiduPcs_autoupdate 百度云自动上传脚本

利用BaiduPCS-Go实现自动备份文件功能，主要配合私人云使用

## 工具简介
通过大佬的BaiduPCS-Go项目。登陆你的百度账号，运行本软件，将会自动周期性的检查你指定的文件夹下文件是否变化，如有变化将会自动上传到百度网盘。
## 使用方法
仅支持linux系统 ，支持多个百度账户使用;
 1. 下载[BaiduPCS-Go](https://github.com/iikira/BaiduPCS-Go),并根据教程登陆你的百度账号获取uid。
 2. 克隆到本地后，编辑config.ini
> [prconfig]<br>
users = 2#用户数目<br>
checktime = 3600 #每隔多久检查一次文件改动并上传<br>
loglocate = /var/log/baidu.log #log存储地址<br>
[user1]<br>
uid = xxxxx #通过BaiduPCS-Go登陆你的账号，获取的uid<br>
upload_path = /root/upload #需要上传的文件(此文件夹下所有文件/文件夹将全部上传)<br>
[user2]<br>
uid = xxxxx #通过BaiduPCS-Go登陆你的账号，获取的uid<br>
upload_path = /root/upload #需要上传的文件(此文件夹下所有文件/文件夹将全部上传)<br>

 3. 使用任何守护进程工具启动checkfile.py即可

### 关于作者
还有其他有趣的小项目会陆续在[这里](https://www.yrblog.cn/ "这里")更新的，希望大家关注。<br>
微信搜索yrtools关注我的公众号，或者下面的二维码。有一些例如京东返利工具的小工具会在上面运行。<br>
[![yrtools](https://www.yrblog.cn/wp-content/uploads/2019/08/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190821220711.png "yrtools")](https://www.yrblog.cn/wp-content/uploads/2019/08/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190821220711.png "yrtools")
 
