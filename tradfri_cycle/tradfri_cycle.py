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

#Cycle between cold and warm color
def cycle ():

    tradfriHub = 'coaps://{}/15001/{}'.format(hubip, panel_id)
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
    time.sleep(0.1)

#query all the available endpoints:
def format_entity(entity):
    return '{}{}{}'.format(str(entity[0]) if len(entity) >= 1 else '', '/' + str(entity[1]) if len(entity) >= 2 else '',
                    '/' + str(entity[2]) if len(entity) >= 3 else '')


def query_entity(entity):
    method = format_entity(entity)
    api = '{} -m get -u "Client_identity" -k "{}" "coaps://{}/{}"'.format(coap, securityid, hubip, method)
    if os.path.exists(coap):
        out = subprocess.check_output(api, shell=True)
        print out.decode("utf-8")
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)


def set_entinty(entity, settings):
    method = format_entity(entity)
    api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "coaps://{}/{}"'.format(coap, securityid, settings, hubip, method)
    if os.path.exists(coap):
        os.popen(api)
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)


def query_all_enpoints():
    #./coap-client -u "Client_identity" -k "YOUR_KEY" -v 10 -m get "coaps://192.168.0.3:5684/.well-known/core"
    method = '.well-known/core'
    api = '{} -m get -u "Client_identity" -k "{}" "coaps://{}/{}"'.format(coap, securityid, hubip, method)
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

        print "========INPUT========"
        print out
        print "=========END=========\n"

        basic_entries = list(set([entry[0] for entry in out]))

        lights = [entry for entry in out if entry[0] == '15001' and len(entry) == 2 and entry[1].isdigit()]
        groups = [entry for entry in out if entry[0] == '15004' and len(entry) == 2 and entry[1].isdigit()]
        scenes = [entry for entry in out if entry[0] == '15005' and len(entry) == 2 and entry[1].isdigit()]
        gateways = [entry for entry in out if entry[0] == '15011' and len(entry) == 2 and entry[1].isdigit()]
        tasks = [entry for entry in out if entry[0] == '15010' and len(entry) == 2 and entry[1].isdigit()]

        print "========LIGHTS======="
        print lights
        print "=========END=========\n"

        print "========GROUPS======="
        print groups
        print "=========END=========\n"

        print "=======SCENES========"
        print scenes
        print "=========END=========\n"

        print "=======GATEWAYS======"
        print gateways
        print "=========END=========\n"

        print "========TASKS========"
        print tasks
        print "=========END=========\n"

        return [basic_entries, lights, groups, scenes, gateways, tasks]
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)

def some_nice_stuff():
    set_entinty(['15001', lightbulb_id], '{"3311":[{"5706":"c984bb"}]}')
    time.sleep(0.3)
    set_entinty(['15001', lightbulb_id], '{"3311":[{"5706":"ebb63e"}]}')
    time.sleep(0.3)
    set_entinty(['15001', lightbulb_id], '{"3311":[{"5706":"e78834"}]}')
    time.sleep(0.3)
    set_entinty(['15001', lightbulb_id], '{"3311":[{"5706":"da5d41"}]}')
    time.sleep(0.3)
    set_entinty(['15001', lightbulb_id], '{"3311":[{"5706":"d9337c"}]}')
    time.sleep(0.3)
    set_entinty(['15001', lightbulb_id], '{"3311":[{"5706":"c984bb"}]}')


def more_stuff1():
    for i in range(0, 255, 3):
        set_entinty(['15004', '154580'], '{"5851":' + str(i) + '}')
        time.sleep(0.75)

def more_stuff2():
    for i in range(0, 255, 3):
        set_entinty(['15001', '65537'], '{"3311":[{"5851":' + str(i) + '}]}')
        time.sleep(0.1)

#while True:
#    cycle()

#change()

#print query_all_enpoints()

#direct_query()

#query_entity(['15004', '154580'])
#query_entity(['15001', '65538'])
#query_entity(['status'])

#devices
#query_entity(['15001', '65538'])
#query_entity(['15001', '65536'])
#query_entity(['15001', '65537'])
#

#group api
#query_entity(['15004', '154580'])
#{"9001":"Nej","9002":1504610855,"9003":154580,"5850":1,"5851":80,"9039":217404,"9018":{"15002":{"9003":[65536,65537,65538]}}}

#device api
#query_entity(['15001', '65538'])
#{"9001":"TRADFRI bulb E27 CWS opal 600lm","9002":1504616889,"9020":1504696103,"9003":65538,"3":{"3":"1.3.002","0":"IKEA of Sweden","1":"TRADFRI bulb E27 CWS opal 600lm","2":"","6":1},"9054":0,"5750":2,"3311":[{"5706":"0","5850":1,"5851":80,"5707":0,"5708":0,"5709":32886,"5710":27217,"5711":0,"9003":0}],"9019":1}

more_stuff2()

# c984bb, ebb63e, e78834, da5d41, d9337c

