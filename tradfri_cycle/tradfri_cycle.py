#!/usr/bin/env python
# tradfri_cycle.py
# A small experiment to cycle colors in a Tradfri LED bulb
# using the Tradfri Gateway. Information retrieved from sources in the
# https://github.com/bwssytems/ha-bridge/issues/570 thread.
# Tord Andersson, 2017-04-25. 

import subprocess
import os
import time
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
def query_entity(entities):
    method = '{}{}'.format(entities[0], '/' + entities[1] if len(entities) == 2 else '')
    api = '{} -m get -u "Client_identity" -k "{}" "coaps://{}"/{}'.format(coap, securityid, hubip, method)
    if os.path.exists(coap):
        out = subprocess.check_output(api, shell=True)
        print out.decode("utf-8")
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)


def query_all_enpoints():
    #./coap-client -u "Client_identity" -k "YOUR_KEY" -v 10 -m get "coaps://192.168.0.3:5684/.well-known/core"
    method = '.well-known/core'
    api = '{} -m get -u "Client_identity" -k "{}" "coaps://{}"/{}'.format(coap, securityid, hubip, method)
    #print api
    #sys.exit()
    if os.path.exists(coap):
        print "======RAW INPUT======"
        out = subprocess.check_output(api, shell=True)
        print out.decode("utf-8")
        print "=========END=========\n"

        out = [item.replace(';ct=0;obs\n', '') for sublist in [x.split(';ct=0,') for x in out.split(';ct=0;obs,')] for item in sublist]
        for i, val in enumerate(out):
            out[i] = out[i].replace('<//', '')
            out[i] = out[i].replace('>', '')
            out[i] = out[i].split('/')

        print "====PARSED INPUT====="
        print out
        print "=========END=========\n"

        lights = [entry for entry in out if entry[0] == '15001' and len(entry) == 2 and entry[1].isdigit()]
        groups = [entry for entry in out if entry[0] == '15004' and len(entry) == 2 and entry[1].isdigit()]
        scenes = [entry for entry in out if entry[0] == '15005' and len(entry) == 2 and entry[1].isdigit()]
        gateways = [entry for entry in out if entry[0] == '15011' and len(entry) == 2 and entry[1].isdigit()]

        combined = lights + groups + scenes + gateways
        print "===PARSED LIGHTS==="
        print lights
        print "=========END=========\n"

        print "====PARSED GROUPS===="
        print groups
        print "=========END=========\n"

        print "====PARSED SCENES===="
        print scenes
        print "=========END=========\n"

        print "====PARSED GATEWAYS===="
        print gateways
        print "=========END=========\n"

        for entity in combined:
            query_entity(entity)

    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)

def direct_query():
    print 'LIGHTS'
    query_entity(['15001'])
    print 'GROUPS'
    query_entity(['15004'])
    print 'SCENES'
    query_entity(['15005'])
    print 'GATEWAYS'
    query_entity(['15011'])
    print 'UNKNOWN'
    query_entity(['15010'])

#while True:
#    cycle()

change()

#query_all_enpoints()

#direct_query()