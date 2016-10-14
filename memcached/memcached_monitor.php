<?php
//php版本memcached监控
$falArr = $data = array();
$conTimeout = 1;
//采集数据
if (extension_loaded('memcached')) {
    $config = array(
        'servers' => array(//服务器组
            array('127.0.0.1', 11211),
        ),
        'policy' => array(//缓存策略
            'compressed' => false, //是否压缩,开启后，默认大于100b时压缩
            'life_time' => 3600, //缓存时间 秒
            'pool' => 'mc', //连接池，同一连接池建立长连接
        )
    );
    $memcached = new \Memcached($config['policy']['pool']);
    $memcached->setOption(\Memcached::OPT_COMPRESSION, $config['policy']['compressed']);
    $memcached->setOption(\Memcached::OPT_CONNECT_TIMEOUT, $conTimeout);
    if ($memcached->addServers($config['servers'])) {
        $data = $memcached->getStats();
    }
}
//要监控的key列表
$monitKeys = array(
    'uptime' => 'GAUGE',
    'threads' => 'GAUGE',
    'pointer_size' => 'GAUGE',
    'rusage_user_seconds' => 'GAUGE',
    'rusage_user_microseconds' => 'GAUGE',
    'rusage_system_seconds' => 'GAUGE',
    'rusage_system_microseconds' => 'GAUGE',
    'curr_items' => 'GAUGE',
    'total_items' => 'GAUGE',
    'limit_maxbytes' => 'GAUGE',
    'curr_connections' => 'GAUGE',
    'total_connections' => 'GAUGE',
    'connection_structures' => 'GAUGE',
    'bytes' => 'GAUGE',
    'cmd_get' => 'GAUGE',
    'cmd_set' => 'GAUGE',
    'get_hits' => 'GAUGE',
    'get_misses' => 'GAUGE',
    'evictions' => 'GAUGE',
    'bytes_read' => 'GAUGE',
    'bytes_written' => 'GAUGE',
);
//关联监控指标数值
foreach ($monitKeys as $k => $v) {
    $falArr[] = array(
        "endpoint" => gethostname(),
        "metric" => "memcached_" . $k,
        "timestamp" => time(),
        "step" => 60,
        "value" => (isset($data[$k]) ? $data[$k] : 0),
        "counterType" => $v,
        "tags" => "project=atido,group=server,name=memcached,method=monitor",
    );
}
//stdOut
echo json_encode($falArr);
