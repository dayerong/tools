## **1. [san_tool.py](https://github.com/dayerong/tools/blob/master/san_tool/san_tool.py)**
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



## **2. [cisco_cfg_backup.py](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup.py)**

```
基于Python 2.7
```

##### ● 为什么写这个脚本？

```
公司网管离职，让我临时代管公司网络，门外汉一个，接手后发现总部、分公司、仓库等各地几百台网络设备的信息都不完整，为了收集这些设备的信息，所以写了这个脚本。
该脚本可以收集Cisco交换机、路由器的相关配置信息，导出到Excel。
另外还有一个收集H3C的脚本，基本上一样。
```

##### ● 脚本用到2个配置文件，cisco_ip_list.txt与command_list.txt，格式如下图：

    cisco_ip_list.txt
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_ip_list.png?raw=true)

<br>

    command_list.txt
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/command_list.png?raw=true)

<br>

##### ● 执行过程见下图：

###### 开始运行
    输入用户名、密码、enable密码。因为我们设置的交换机密码都一样，如果各不相同，那就要另外的写法了。
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_1.png?raw=true)

###### 运行结束
    在当前目录下会创建output目录，该目录下会生成每台设备的命令执行结果。
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_2.png?raw=true)

<br>

![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_3.png?raw=true)

<br>
<br>
    另外生成一个Excel表，3张sheet分别为收集是否成功、输出文件信息、硬件配置信息（主机名、IP、型号、序列）

![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_4.png?raw=true)
<br>
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_5.png?raw=true)
<br>
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_6.png?raw=true)
<br>
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_7.png?raw=true)