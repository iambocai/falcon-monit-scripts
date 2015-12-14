#!/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'iambocai'

import sys, urllib2, base64, json, time,socket


step = 60
ip = socket.gethostname()
ts = int(time.time())
keys = ('messages_ready', 'messages_unacknowledged')
rates = ('ack', 'deliver', 'deliver_get', 'publish')

request = urllib2.Request("http://%s:15672/api/queues" %ip)
# see #issue4
base64string = base64.encodestring('guest:guest')
request.add_header("Authorization", "Basic %s" % base64string)   
result = urllib2.urlopen(request)
data = json.loads(result.read())
tag = ''
#tag = sys.argv[1].replace('_',',').replace('.','=')

p = []
for queue in data:
	# ready and unack
	msg_total = 0
	for key in keys:
		q = {}
		q["endpoint"] = ip
		q['timestamp'] = ts
		q['step'] = step
		q['counterType'] = "GAUGE"
		q['metric'] = 'rabbitmq.%s' % key
		q['tags'] = 'name=%s,%s' % (queue['name'],tag)
		q['value'] = int(queue[key])
		msg_total += q['value']
		p.append(q)

	# total
	q = {}
	q["endpoint"] = ip
	q['timestamp'] = ts
	q['step'] = step
	q['counterType'] = "GAUGE"
	q['metric'] = 'rabbitmq.messages_total'
	q['tags'] = 'name=%s,%s' % (queue['name'],tag)
	q['value'] = msg_total
	p.append(q)
	
	# rates
	for rate in rates:
		q = {}
		q["endpoint"] = ip
		q['timestamp'] = ts
		q['step'] = step
		q['counterType'] = "GAUGE"
		q['metric'] = 'rabbitmq.%s_rate' % rate
		q['tags'] = 'name=%s,%s' % (queue['name'],tag)
		try:
			q['value'] = int(queue['message_stats']["%s_details" % rate]['rate'])
		except:
			q['value'] = 0
		p.append(q)

print json.dumps(p, indent=4)


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

# check. Substitute with appropriate HTTP code.
if connection.code == 200:
    print connection.read()
else:
    print '{"err":1,"msg":"%s"}' % connection
