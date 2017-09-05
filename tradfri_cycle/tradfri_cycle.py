#!/usr/bin/env python
# tradfri_cycle.py
# A small experiment to cycle colors in a Tradfri LED bulb
# using the Tradfri Gateway. Information retrieved from sources in the
# https://github.com/bwssytems/ha-bridge/issues/570 thread.
# Tord Andersson, 2017-04-25. 

import subprocess
import os
import time
import math
import sys


status, output = subprocess.call('dig +short myip.opendns.com @resolver1.opendns.com', shell=True)
hubip = output.strip()

coap = '/usr/local/bin/coap-client'

#Update to match your equipment
securityid = 'USE_STICKER_KEY'
lightbulbid = '65537'

tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)

#Light on
payload = '{ "3311": [{ "5850": 1 }] }'
api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "{}"' .format(coap, securityid, payload, tradfriHub)
if os.path.exists(coap):
    os.popen(api)
else:
    sys.stderr.write('[-] libcoap: could not find libcoap\n')
    sys.exit(1)

#Cycle between cold and warm color
while True:
    time_s = time.time()
    scale_factor = (time_s % 10)/5
    if scale_factor > 1:
        scale_factor = 2 - scale_factor
    print "time: %f scale factor: %f" % (time_s, scale_factor) 
    x = 24930 + int(8205 * scale_factor)
    y = 24684 + int(2527 * scale_factor)
    print "X:", x
    print "Y:", y
    payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % (x, y)
    api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "{}"' .format(coap, securityid, payload, tradfriHub)
    if os.path.exists(coap):
        os.popen(api)
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    time.sleep(0.01)

