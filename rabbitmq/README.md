open-falcon rabbitmq监控脚本
================================

系统需求
--------------------------------
操作系统：Linux
Python >= 2.6
python-simplejson

主要逻辑
--------------------------------
从rabbitmq-server的api接口读取相关数据，然后推送到falco-agent

汇报字段
--------------------------------
| key |  tag | type | note |
|-----|------|------|------|
|rabbitmq.messages_ready|name(Queue名字)|GAUGE|队列中处于等待被消费状态消息数|
|rabbitmq.messages_unacknowledged|name(Queue名字)|GAUGE|队列中处于消费中状态的消息数|
rabbitmq.messages_total|name(Queue名字)|GAUGE|队列中所有未完成消费的消息数，等于messages_ready+messages_unacknowledged|
rabbitmq.ack_rate|name(Queue名字)|GAUGE|消费者ack的速率|
rabbitmq.deliver_rate|name(Queue名字)|GAUGE|deliver的速率|
rabbitmq.deliver_get_rate|name(Queue名字)|GAUGE|deliver_get的速率|
rabbitmq.publish_rate|name(Queue名字)|GAUGE|publish的速率|


使用方法
--------------------------------
1. 根据实际部署情况，修改15,16行的rabbitmq-server管理端口和登录用户名密码
2. 确认1中配置的rabbitmq用户有你想监控的queue/vhosts的权限
3. 将脚本加入crontab即可


授权类型：MIT
