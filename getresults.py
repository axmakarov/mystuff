#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
f1 = open('D:\\jsonrequest2.txt', 'w+')
queueId = "e01b7dc3-87ef-43d8-942b-2a0b14bc0e94"
uid = "5b275d6e-ddf5-11e4-8d57-94de80b0451a"
payload = {"jsonrpc":"2.0","method":"getQueueResult","params":{"token":"2b4298c7-ac6c-11e4-8222-50465d9ff9a8","id":queueId},"id":uid}
payload = json.dumps(payload)
print >>f1, payload
