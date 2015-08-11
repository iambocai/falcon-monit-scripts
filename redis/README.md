open-falcon redis监控脚本
================================

系统需求
--------------------------------
操作系统：Linux

Python >= 2.6

python-simplejson

主要逻辑
--------------------------------
根据搜索到的redis配置文件，依次从文件中取出redis实例的端口号号和密码，然后使用telnetlib telnet相应端口
发送auth和info命令，解析返回结果，最后将关心的key组装成json后push到falcon-agent

汇报字段
--------------------------------
| key |  tag | type | note |
|-----|------|------|------|
|redis.connected_clients|port|GAUGE|已连接客户端的数量|
|redis.blocked_clients|port|GAUGE|正在等待阻塞命令（BLPOP、BRPOP、BRPOPLPUSH）的客户端的数量|
|redis.used_memory|port|GAUGE|由 Redis 分配器分配的内存总量，以字节（byte）为单位|
|redis.used_memory_rss|port|GAUGE| 从操作系统的角度，返回 Redis 已分配的内存总量（俗称常驻集大小）|
|redis.mem_fragmentation_ratio|port|GAUGE|used_memory_rss 和 used_memory 之间的比率|
|redis.total_commands_processed|port|COUNTER|采集周期内执行命令总数|
|redis.rejected_connections|port|COUNTER|采集周期内拒绝连接总数|
|redis.expired_keys|port|COUNTER|采集周期内过期key总数|
|redis.evicted_keys|port|COUNTER|采集周期内踢出key总数|
|redis.keyspace_hits|port|COUNTER|采集周期内key命中总数|
|redis.keyspace_misses|port|COUNTER|采集周期内key拒绝总数|
|redis.keyspace_hit_ratio|port|GAUGE|访问命中率|

如需增减字段，请修改monit_keys变量

使用方法
--------------------------------
1. 根据实际部署情况，修改有注释位置附近的配置
2. 测试： python redis-monitor.py
3. 将脚本加入crontab执行即可


授权类型：MIT
