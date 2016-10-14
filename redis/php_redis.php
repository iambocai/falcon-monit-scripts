<?php

/**
 * memcached监控
 * 监控频率60s
 *
 * @user 刘松森 <liusongsen@gmail.com>
 * @date 16/7/29
 */

$falArr = $data = array();
$conTimeout = 1;
//采集数据
if (extension_loaded('memcached')) {
    $redis = new \Redis();
    if ($result = $redis->connect("192.168.0.115", 6379, $conTimeout)) {
        $data = $redis->info();
        $redis->close();
    }
}
//要监控的key列表
$monitKeys = array(
    'connected_clients' => 'GAUGE',
    'blocked_clients' => 'GAUGE',
    'used_memory' => 'GAUGE',
    'used_memory_rss' => 'GAUGE',
    'mem_fragmentation_ratio' => 'GAUGE',
    'total_commands_processed' => 'COUNTER',
    'rejected_connections' => 'COUNTER',
    'expired_keys' => 'COUNTER',
    'evicted_keys' => 'COUNTER',
    'keyspace_hits' => 'COUNTER',
    'keyspace_misses' => 'COUNTER',
    'keyspace_hit_ratio' => 'GAUGE',
);
//关联监控指标数值
foreach ($monitKeys as $k => $v) {
    $falArr[] = array(
        "endpoint" => gethostname(),
        "metric" => "redis_" . $k,
        "timestamp" => time(),
        "step" => 60,
        "value" => (isset($data[$k]) ? $data[$k] : 0),
        "counterType" => $v,
        "tags" => "project=atido,group=server,name=redis,method=monitor",
    );
}
//stdOut
echo json_encode($falArr);
