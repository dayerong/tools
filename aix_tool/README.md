#### **[nim_tool.sh](https://github.com/dayerong/tools/blob/master/san_tool/san_tool.py)**

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
║               NIM Master远程命令执行工具                 ║
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
║               NIM Master远程命令执行工具                 ║
║                                                         ║
╚=========================================================╝
----------NIM客户端----------
wms1

请输入需要执行的命令：hostname      <-----
wms1


返回：（q）    继续：（Enter）
╔=========================================================╗
║                                                         ║
║               NIM Master远程命令执行工具                 ║
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
║               NIM Master远程命令执行工具                 ║
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

#### **[nim_backup.sh](https://github.com/dayerong/tools/blob/master/aix_tool/nim_backup.sh)**

``` 
适用于AIX操作系统
```

- 为什么写这个脚本？

```
1. 此脚本主要通过NIM Master Server对NIM Client进行系统备份（mksysb）。
2. 手工选择需要备份的client，备份成功保存备份记录。
3. NIM的功能真的非常强大，安装、升级、迁移、恢复等等无所不能。
```

- 脚本执行输出如下：

```
[nimsvrtst]/nimdata/script>#./nim_backup.sh 
╔=========================================================╗
║                                                         ║
║               NIM Master远程备份执行工具                 ║
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

警告：本工具用于客户端的系统备份。
退出：（q）

请选择：2
╔=========================================================╗
║                                                         ║
║               NIM Master远程备份执行工具                 ║
║                                                         ║
╚=========================================================╝
----------NIM客户端----------
wms1

将发起对wms1的备份命令，确认（y/n）? y

wms1备份开始...

+---------------------------------------------------------------------+
                System Backup Image Space Information
              (Sizes are displayed in 1024-byte blocks.)
+---------------------------------------------------------------------+

Required = 18300744 (17872 MB)    Available = 866896892 (846579 MB)



Creating information file (/image.data) for rootvg.

Creating list of files to back up.
.
Backing up 102488 files..............................
59969 of 102488 files (58%)..............................
86430 of 102488 files (84%)..............................
92170 of 102488 files (89%)......

102488 of 102488 files (100%)
0512-038 savevg: Backup Completed Successfully.

wms1备份成功。


返回：（q）q
╔=========================================================╗
║                                                         ║
║               NIM Master远程备份执行工具                 ║
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

警告：本工具用于客户端的系统备份。
退出：（q）

请选择：q
[nimsvrtst]/nimdata/script>#cd ../os_backup/
[nimsvrtst]/nimdata/os_backup>#cat mksysb.history 
IP                      Hostname        Start Time                      End Time
===========================================================================================
192.168.60.122          wms2            2016/04/20-10:05:48             2016/04/20-10:13:20
192.168.60.122          wms2            2016/04/20-10:48:53             2016/04/20-10:56:07
192.168.58.115          momdg           2016/06/17-09:37:02             2016/06/17-09:47:16
192.168.60.120          wms1            2016/08/31-12:06:33             2016/08/31-12:21:39
192.168.58.184          datahub         2016/08/31-12:24:13             2016/08/31-12:37:40
192.168.60.122          wms2            2016/08/31-13:17:40             2016/08/31-13:29:52
192.168.0.128           wmsdb2          2016/08/31-13:37:12             2016/08/31-13:49:47
192.168.58.163          bipas1          2017/03/31-12:38:17             2017/03/31-12:47:11
192.168.60.120          wms1            2017/05/11-16:29:45             2017/05/11-16:47:38  <-----
[nimsvrtst]/nimdata/os_backup>#ls -ltr
total 4436376
-rw-r--r--    1 root     system        11860 Jul 13 2017  wms1_image.data
-rw-r--r--    1 root     system   15526860800 May 11 16:47 wms1_mksysb_20170511  <-----
-rw-r--r--    1 root     system         3172 May 11 16:47 mksysb.history
[nimsvrtst]/nimdata/os_backup>#


```


