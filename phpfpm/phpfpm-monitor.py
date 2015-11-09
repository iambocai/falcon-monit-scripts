#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'serika00'

import commands, socket, time, json, urllib2
#import sys

STATUS_PATH = "/fpm/status"
LISTEN_ADDR = "127.0.0.1:9000"

def go():
    monit_keys = [
        # 'pool
        # 'start_time'
        # 'process_manager'
        # 'start_since'
        ('active_processes', 'GAUGE'),
        ('accepted_conn', 'COUNTER'),
        ('listen_queue', 'GAUGE'),
        ('idle_processes', 'GAUGE'),
        ('slow_requests', 'GAUGE'),
        ('max_active_processes', 'GAUGE'),
        ('max_children_reached', 'GAUGE'),
        ('max_listen_queue', 'GAUGE'),
        ('total_processes', 'GAUGE'),
        ('listen_queue_len', 'GAUGE'),
    ]

    status = commands.getoutput("SCRIPT_NAME=%s SCRIPT_FILENAME=%s QUERY_STRING='json' REQUEST_METHOD=GET cgi-fcgi -bind -connect %s | tail -n 1" % (STATUS_PATH, STATUS_PATH, LISTEN_ADDR))
    status = json.loads(status)

    ip = socket.gethostname()
    timestamp = int(time.time())
    step = 60
    metric = 'php'
    endpoint = ip
    tags = 'pool=%s' % status['pool']
    p = []

    for key, vtype in monit_keys:
        value = int(status[key.replace('_', ' ')])
        i = {
            'Metric': '%s.%s' % (metric, key),
            'Endpoint': endpoint,
            'Timestamp': timestamp,
            'Step': step,
            'Value': value,
            'CounterType': vtype,
            'TAGS': tags
        }
        p.append(i)

    #print json.dumps(p)
    #sys.exit(0)
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = 'http://127.0.0.1:1988/v1/push'
    request = urllib2.Request(url, data=json.dumps(p) )
    request.add_header("Content-Type",'application/json')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    if connection.code == 200:
        pass
    else:
        print '{"err":1,"msg":"%s"}' % connection

if __name__ == '__main__':
    go()
