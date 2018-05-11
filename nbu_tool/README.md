#### **[nbu_policy.sh](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup.py)**


- 为什么写这个脚本？

```
1. 公司使用Veritas NetBackup作为备份系统，接手第一件事情就是去整理备份策略，但几百条的策略手工去整理非常费时间，问过原厂有没有相关的工具直接导出所有策略生成表格，回复说没有。最后想想还是写个脚本，一劳永逸，每次更新策略不用再去同时更新表格了。

2. 一开始想导出到Excel，但由于DBA有时也要查询备份策略的定制，最后脚本是导入到数据库，通过一个简单的页面展示出来的。

```

- 脚本格式很简单，其实就是过滤和处理字符串，awk+sed，有点难看。准备用Python写一个直接导出到Excel。


- 生成的页面如截图：

![image](https://github.com/dayerong/tools/blob/master/cisco_tool/cisco_cfg_backup_7.png?raw=true)