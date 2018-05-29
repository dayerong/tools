#### **[san_info.py](https://github.com/dayerong/tools/blob/master/san_info/san_info.py)**

``` 
基于Python 2.7
```

- 脚本功能

```
主要是用来收集SAN交换机（Brocade及OEM Brocade）的硬件信息、端口信息等，导出生成Excel。
```


- 脚本用到一个[swinfo.ini](https://github.com/dayerong/tools/blob/master/san_tool/swinfo.ini)配置文件，格式如下：

```
[account]
sw_user = admin
sw_password = admin

[switch]
sw_ip = 192.168.58.24,192.168.58.25,192.168.187.109
```

- 脚本会检测网络能否到达交换机、检测用户登录数是否超过最大限制、检测用户密码的正确性。


- 执行过程如下：

```
D:\GitHub\tools\san_info>python san_info.py

Information is being collected ...

[192.168.58.24]  Successful and time elapsed: 9.17s
[192.168.58.25]  Successful and time elapsed: 9.17s
[192.168.187.116]  Successful and time elapsed: 8.36s
[192.168.187.119]  Successful and time elapsed: 5.63s
[192.168.187.120]  Successful and time elapsed: 7.61s
[192.168.187.121]  Successful and time elapsed: 16.23s
[192.168.187.11]  Unable to connect!

Complete and time elapsed: 58.19s

D:\GitHub\tools\san_info>
```

- 执行完成会生成一个文件： ++SAN交换机设备配置信息.xls++


![image](https://github.com/dayerong/tools/blob/master/san_info/san_info_1.png?raw=true)
![image](https://github.com/dayerong/tools/blob/master/san_info/san_info_.png?raw=true)

---