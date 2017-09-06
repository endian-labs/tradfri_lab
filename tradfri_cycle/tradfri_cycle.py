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

coap = '/usr/local/bin/coap-client'

#Update to match your equipment
securityid = 'E4QjQ03vBi9JVFhX'
hubip = '192.168.2.188:5684'
lightbulb_id = '65538'
panel_id = '65537'

tradfriHub = 'coaps://{}/15001/{}'.format(hubip, lightbulb_id)

#Light on
payload = '{ "3311": [{ "5850": 1 }] }'
api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "{}"' .format(coap, securityid, payload, tradfriHub)
if os.path.exists(coap):
    os.popen(api)
else:
    sys.stderr.write('[-] libcoap: could not find libcoap\n')
    sys.exit(1)

def change ():
    payload = '{"3311":[{"5706":"d9337c"}]}'
    api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "{}"'.format(coap, securityid, payload, tradfriHub)
    if os.path.exists(coap):
        print "======START======"
        out = subprocess.check_output(api, shell=True)
        print out.decode("utf-8")
        print "=======END======="
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    sys.exit()

#Cycle between cold and warm color
def cycle ():
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
        print "======START======"
        out = subprocess.check_output(api, shell=True)
        print out.decode("utf-8")
        print "=======END======="
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    time.sleep(0.5)

#query all the available endpoints:
def query_all_enpoints():
    #./coap-client -u "Client_identity" -k "YOUR_KEY" -v 10 -m get "coaps://192.168.0.3:5684/.well-known/core"
    #/usr/local/bin/coap-client -m get -u "Client_identity" -k "E4QjQ03vBi9JVFhX" "coaps://192.168.2.188/.well-known/core"
    api = '{} -m get -u "Client_identity" -k "{}" "{}"'.format(coap, securityid, 'coaps://' + hubip + '/.well-known/core')
    #print api
    #sys.exit()
    if os.path.exists(coap):
        print "======START======"
        out = subprocess.check_output(api, shell=True)
        print out.decode("utf-8")
        print "=======END======="
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    sys.exit()

#while True:
#    cycle()

change()

#query_all_enpoints()
