# shell定时器命令

## 1、编辑定时器任务：

crontab  -e



## 2、几个示例：

1. [root@hyserver ~]# cd/etc/init.d/

          [root@hyserverinit.d]# crontab –e

        在root文件后面添加一行（含义：每隔十分钟执行一次脚本）

           0,10,20,30,40,50 * * * * /temp/timer.sh

2. 修改脚本的权限：

          chmod  777 /temp/timer.sh

3. 设置完了之后不要忘了，启动定时服务（大多数忘了这里）

        [root@hyserver init.d]# service crond stop

        [root@hyserver init.d]# service crond start

 备注：Crontab第一道第五个字段的整数取值范围及意义是：

       0～59 表示分

      1～23 表示小时

      1～31 表示日

      1～12 表示月份

      0～6 表示星期（其中0表示星期日）
