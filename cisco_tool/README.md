#### **[cisco_cfg_backup.py](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup.py)**

```
基于Python 2.7
```

- 为什么写这个脚本？

```
公司网管离职，让我临时代管公司网络，门外汉一个，接手后发现总部、分公司、仓库等各地几百台网络设备的信息都不完整，为了收集这些设备的信息，所以写了这个脚本。
该脚本可以收集Cisco交换机、路由器的相关配置信息，导出到Excel。
另外还有一个收集H3C的脚本，基本上一样。
```

- 脚本用到2个配置文件，cisco_ip_list.txt与command_list.txt，格式如下图：

<br>

    cisco_ip_list.txt
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_ip_list.png?raw=true)

<br>

    command_list.txt
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/command_list.png?raw=true)


<br>

- 执行过程见下图：

###### 开始运行
    输入用户名、密码、enable密码。因为我们设置的交换机密码都一样，如果各不相同，那就要另外的写法了。
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_1.png?raw=true)

###### 运行结束
    在当前目录下会创建output目录，该目录下会生成每台设备的命令执行结果。


    另外生成一个Excel表，3张sheet分别为收集是否成功、输出文件信息、硬件配置信息（主机名、IP、型号、序列号）

![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_6.png?raw=true)
<br>
![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_7.png?raw=true)


---
