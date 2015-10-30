#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'iambocai'

import requests
import json
import time
import socket
import os
import re
import telnetlib
import sys
import commands

class MemcachedStats:

    _client = None
    _key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(ur'STAT items:(.*):number')
    _stat_regex = re.compile(ur"STAT (.*) ([0-9]+\.?[0-9]*)\r")

    def __init__(self, host='localhost', port='11211'):
        self._host = host
        self._port = port

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write("%s\n" % cmd)
        return self.client.read_until('END')

    def close(self):
        'close telnet connection'
        return self.client.write("quit\n")

    def key_details(self, sort=True, limit=100):
        ' Return a list of tuples containing keys and details '
        cmd = 'stats cachedump %s %s'
        keys = [key for id in self.slab_ids()
            for key in self._key_regex.findall(self.command(cmd % (id, limit)))]
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True, limit=100):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort, limit=limit)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))


def main():
    ip = socket.gethostname()
    timestamp = int(time.time())
    step = 60
    insts_list = [ os.path.basename(i) for i in commands.getoutput(''' ps -ef |grep memcached|grep -v grep |sed -n 's/.* *-p *\([0-9]\{1,5\}\).*/\1/p' ''' ).split('\n') ]
    data = []

    gauges = [ 'get_hit_ratio', 'incr_hit_ratio', 'decr_hit_ratio', 'delete_hit_ratio', 'usage', 'curr_connections', 'total_connections', 'bytes', 'pointer_size', 'uptime', 'limit_maxbytes', 'threads', 'curr_items', 'total_items', 'connection_structures' ]
  
    for inst in insts_list:
        
        port = inst
        metric = "memcached"
        endpoint = ip
        tags = 'port=%s' % port

        try:
            # ATT: if your instance listened on 127.0.0.1, change "ip" to "127.0.0.1" in follow line
            conn = MemcachedStats(ip, port)
            stats = conn.stats()
            conn.close()
        except:
            continue

        del stats['pid']
        del stats['time']

        stats['usage'] = str(100 * float(stats['bytes']) / float(stats['limit_maxbytes']))
        try:
            stats['get_hit_ratio'] = str(100 * float(stats['get_hits']) / (float(stats['get_hits']) + float(stats['get_misses'])))
        except ZeroDivisionError:
            stats['get_hit_ratio'] = '0.0'
        try:
            stats['incr_hit_ratio'] = str(100 * float(stats['incr_hits']) / (float(stats['incr_hits']) + float(stats['incr_misses'])))
        except ZeroDivisionError:
            stats['incr_hit_ratio'] = '0.0'
        try:
            stats['decr_hit_ratio'] = str(100 * float(stats['decr_hits']) / (float(stats['decr_hits']) + float(stats['decr_misses'])))
        except ZeroDivisionError:
            stats['decr_hit_ratio'] = '0.0'
        try:
            stats['delete_hit_ratio'] = str(100 * float(stats['delete_hits']) / (float(stats['delete_hits']) + float(stats['delete_misses'])))
        except ZeroDivisionError:
            stats['delete_hit_ratio'] = '0.0'


        for key in stats:
            value  = float(stats[key])
            if key in gauges:
                suffix = ''
                vtype  = 'GAUGE'
            else:
                suffix = '_cps'
                vtype = 'COUNTER'

            i = {
                'metric': '%s.%s%s' % (metric, key, suffix),
                'endpoint': endpoint,
                'timestamp': timestamp,
                'step': step,
                'value': value,
                'counterType': vtype,
                'tags': tags
            }
            data.append(i)

    return data
    

if __name__ == '__main__':
    proc = commands.getoutput(''' ps -ef|grep 'memcached-monitor.py'|grep -v grep|wc -l ''')
    if int(proc) < 3:
        r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(main()))
        print r.text
