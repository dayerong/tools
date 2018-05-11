#### **[nbu_policy.sh](https://github.com/dayerong/tools/blob/master/nbu_tool/nbu_policy.sh)**


- 为什么写这个脚本？

```
1. 公司使用Veritas NetBackup作为备份系统，接手第一件事情就是去整理备份策略，但几百条的策略手工去整理非常费时间，问过原厂有没有相关的工具直接导出所有策略生成表格，回复说没有。最后想想还是写个脚本，一劳永逸，每次更新策略不用再去同时更新表格了。

2. 一开始想导出到Excel，但由于DBA有时也要查询备份策略的信息，最后脚本是导入到数据库，通过一个简单的PHP页面展示出来的。

```

- 脚本格式很简单，其实就是过滤和处理字符串，awk+sed，有点难看，准备用Python写一个直接导出到Excel。

- 虽然脚本难看，但真的很实用，省了很多精力，每次简单执行脚本就能生成最新的策略信息，很爽。

- 创建表的SQL


```
Create Table: CREATE TABLE `nbu_policy` (
  `ID` mediumint(9) NOT NULL AUTO_INCREMENT,
  `Policy_Name` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `Policy_Type` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `Policy_Status` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `Volume_Pool` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `Client_Name` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `Client_IP` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `Hardware` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `OS` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `Backup_Type` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `Retention_Level` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `Frequency` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `Backup_Windows` varchar(1000) COLLATE utf8_bin DEFAULT NULL,
  `Content` varchar(300) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin
```

- 生成的页面如截图：

![image](https://github.com/dayerong/tools/blob/master/nbu_tool/nbu_policy.png?raw=true)
