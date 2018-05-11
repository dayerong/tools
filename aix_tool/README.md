#### **[nim_tool.sh](https://github.com/dayerong/tools/blob/master/aix_tool/nim_tool.sh)**

``` 
适用于AIX操作系统
```

- 为什么写这个脚本？

```
1. AIX操作系统默认没有安装ssh，无法做服务器间的ssh信任，这样就无法通过免密码远程执行命令。
2. 此脚本主要通过NIM Master Server对NIM Client进行命令的远程执行。
3. 事先配置好nim server，添加nim client。（通常使用到AIX的都会用到nim server）
4. 其实我用到最多的是当忘记了root密码，通过它去重置密码。（AIX下忘记root密码比Linux下恢复起来麻烦很多）
```


- 脚本执行输出如下：

```
[nimsvrtst]/nimdata/script>#sh nim_tool.sh
╔=========================================================╗
║                                                         ║
║               NIM Master远程命令执行工具                ║
║                                                         ║
╚=========================================================╝

----------NIM客户端----------
(1)  dapormfpip     
(2)  wms1           
(3)  wms2           
(4)  wmsdb2         
(5)  wmsdb_129      
(6)  wmsdb1         
(7)  dpebs          
(8)  momas1         
(9)  rmsas1         
(10) momdb1         
(11) momas2         
(12) DPEBSDG        
(13) rmsas2         
(14) momdb2         
(15) dpebsr12       
(16) bipas1         
(17) datahub        
(18) dapoapip       
(19) momdg          
(20) dpebsr12test   
(21) viosrv1        
(22) momdb1tst      
(23) dposdg         
(24) ebsr12dg       
(25) wmsdg          
(26) crmdb1tst      
(27) wmsdb3tst      
(28) dpebsbak       

警告：由于本工具对客户端具有root权限，请谨慎执行命令！
退出：（q）

请选择：2
╔=========================================================╗
║                                                         ║
║               NIM Master远程命令执行工具                ║
║                                                         ║
╚=========================================================╝
----------NIM客户端----------
wms1

请输入需要执行的命令：hostname      <-----
wms1


返回：（q）    继续：（Enter）
╔=========================================================╗
║                                                         ║
║               NIM Master远程命令执行工具                ║
║                                                         ║
╚=========================================================╝
----------NIM客户端----------
wms1

请输入需要执行的命令：df -g          <-----
Filesystem    GB blocks      Free %Used    Iused %Iused Mounted on
/dev/hd4          20.00     11.88   41%    15822     1% /
/dev/hd2           8.00      2.84   65%    49938     7% /usr
/dev/hd9var        8.00      7.48    7%     8079     1% /var
/dev/hd3           8.00      7.62    5%     1134     1% /tmp
/dev/hd1          50.00     46.40    8%    20225     1% /home
/dev/hd11admin      1.00      1.00    1%        7     1% /admin
/proc                 -         -    -         -     -  /proc
/dev/hd10opt       1.00      0.77   24%     7173     4% /opt
/dev/livedump      0.50      0.50    1%        4     1% /var/adm/ras/livedump
/dev/fslv00      130.00     44.34   66%   116481     2% /u01


返回：（q）    继续：（Enter）q
╔=========================================================╗
║                                                         ║
║               NIM Master远程命令执行工具                ║
║                                                         ║
╚=========================================================╝

----------NIM客户端----------
(1)  dapormfpip     
(2)  wms1           
(3)  wms2           
(4)  wmsdb2         
(5)  wmsdb_129      
(6)  wmsdb1         
(7)  dpebs          
(8)  momas1         
(9)  rmsas1         
(10) momdb1         
(11) momas2         
(12) DPEBSDG        
(13) rmsas2         
(14) momdb2         
(15) dpebsr12       
(16) bipas1         
(17) datahub        
(18) dapoapip       
(19) momdg          
(20) dpebsr12test   
(21) viosrv1        
(22) momdb1tst      
(23) dposdg         
(24) ebsr12dg       
(25) wmsdg          
(26) crmdb1tst      
(27) wmsdb3tst      
(28) dpebsbak       

警告：由于本工具对客户端具有root权限，请谨慎执行命令！
退出：（q）

请选择：q
[nimsvrtst]/nimdata/script>#
```


---
