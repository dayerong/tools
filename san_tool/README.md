## **[san_tool.py](https://github.com/dayerong/tools/blob/master/san_tool/san_tool.py)**

``` 
基于Python 2.7
```

##### ● 为什么写这个脚本？

```
这个脚本主要是用来查询SAN交换机（Brocade及OEM Brocade）的端口信息。我工作中由于有数十台SAN交换机，当要查找某台服务器HBA卡或是某台存储的控制器连在哪台交换机的哪个端口，我之前通常会去查Excel表，可这个表可能会出现更新不及时的情况，且查询比较繁琐。所以写了这个脚本，方便快速定位端口。
```


##### ● 脚本用到一个[swinfo.ini](https://github.com/dayerong/tools/blob/master/san_tool/swinfo.ini)配置文件，格式如下：

```
[account]
sw_user = admin
sw_password = admin

[switch]
sw_ip = 192.168.58.24,192.168.58.25,192.168.187.109
```

##### ● 脚本会先检测网络能否到达交换机、检测用户登录数是否超过最大限制。没有做用户名及密码的检测，因为做的时候老是出现一点问题，后来就取消掉了。


##### ● 支持HBA卡wwn格式：

```
"10000090FA5AE006"
"10:00:00:90:fa:5a:e0:06"
```


##### ● 不会GUI，界面很丑，截图如下：

###### 开始运行
![image](https://raw.githubusercontent.com/dayerong/tools/master/san_tool/san_tool_1.png)

###### 查询结束
![image](https://raw.githubusercontent.com/dayerong/tools/master/san_tool/san_tool_2.png)


---