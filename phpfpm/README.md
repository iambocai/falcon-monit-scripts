open-falcon php-fpm监控脚本
===========================

安装使用(Ubuntu)
--------

`sudo apt-get install fcgiwrap`

php-fpm设置`pm.status_path`，与脚本中设置相应，并填上php-fpm监控地址或sock文件。

加入crontab中定时执行。

汇报字段
--------
| key | tag | type | note |
|-----|-----|------|------|
|php.active_process|pool|GAUGE|活跃进程数|
|php.accepted_conn|pool|GAUGE|接受请求数|
|php.listen_queue|pool|GAUGE||
|php.idle_processes|pool|GAUGE|空闲进程数|
|php.slow_requests|pool|GAUGE|慢请求数|
|php.max_active_processes|pool|GAUGE|达到的最大活跃进程数|
|php.max_children_reqched|pool|GAUGE|达到的最大子进程数|
|php.max_listen_queue|pool|GAUGE|达到的最大请求队列数|
|php.total_processes|pool|GAUGE|总进程数|
|php.listen_queue_len|pool|GAUGE||


授权类型：MIT
