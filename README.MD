Tradfri lab
===========

Experimental code to access IKEA tradfri devices.

Protocol Stack
--------------
According to sources (https://github.com/bwssytems/ha-bridge/issues/570), 
IKEA Tradfri uses the following protocol stack:

* OMA Lightweight M2M
* CoAP DTLS/UDP
* Zigbee Light Link 

CoAP build and install
----------------------
A small script, create_coap_w_dtls.sh, has been written to build and install CoAP with DTLS on a debian/raspbian Linux host.

tradfri_cycle.py
----------------
Small python script to experiment with color cycling in an IKEA Tradfri LED bulb.
Change bulb number, key and IP address to match your equiment.

Note! No warranties of any kind! :)

/Tord Andersson, 2017-05-16
 
