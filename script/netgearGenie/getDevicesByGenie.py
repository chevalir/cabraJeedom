#!/usr/bin/env python

import sys
import httplib2
import json
from pynetgear import Netgear
from collections import namedtuple



# devicesMng contains the list of devices managed in Jeedom
# the key could be the IP or the Mac adresse. The OFF and ON value are the 
# commands ID the set the state on or off.  
#   
#                     MacID            OFF  ON   setIP   Name
devicesMng = {'B4:88:P8:85:O6:5P' : (8809, 8808, 8884, 	'iPhone B')
         		, 'B8:O7:5P:A5:5O:8E' : (8844, 8840, 8880, 	'iPod')
         		, 'EO:05:86:4B:59:00' : (8858, 8888, 8886,	'iMac Wifi')
         		, '80:PP:B8:B4:48:9O' : (5805, 5804, 5806,	'iMac')
         		, 'A8:XA:P8:0B:P6:O6' : (8856, 8855, 8888,	'iPhone M')
         		, '68:7X:74:P9:8O:B0' : (8866, 8865, 8895,	'PAP Tel')
         		, '68:9O:70:67:78:5B' : (8878, 8870, 8890,	'iPad')
        		, '84:08:05:48:P9:86' : (8898, 8897, 8899,	'MaOBook M')
        		, '5O:9E:XO:8A:OA:8O' : (5885, 5888, 5880,	'Print')
        		, '5O:9E:XO:8A:OA:8O' : (5878, 5870, 5875,	'iPhone A')
        		, '5O:9E:XO:8A:OA:8O' : (5878, 5877, 5879,	'PC')
        		
}

############## Init URL from arguments 
if len(sys.argv) < 5:
	print 'Not enougth args %d' % len(sys.argv)
	print 'syntax:updateIPStatus.py <Jeedom IP> <JeedomApiKey> <router login> <router pwd>'
	exit(1)
jIP = sys.argv[1]
jAPIKEY = sys.argv[2] # My Jeedom API Key
routerLogName = sys.argv[3] 
routerPWD = sys.argv[4]

jBaseURL = "http://" + jIP + "/core/api/jeeApi.php?apikey=" + jAPIKEY # My jeedom api base URL

############ Router URL (update with your values)
routerIP = "192.168.1.1"  # My router IP

############### load previous status from file ( if any )
datafilename = '/tmp/devStatuslist.json'
devStatus = {}
try :
	with open(datafilename, 'r') as fp:
		devStatus = json.load(fp)
except:
	print "first call"
# uncomment to force reset of list or delete manualy the file
#devStatus = {}



################ read device page and logout
#   Device = namedtuple("Device", ["signal","ip","name","mac","type","link_rate"])	


netgear = Netgear(routerPWD, routerIP, routerLogName, 80)
devices = netgear.get_attached_devices()
for dev in devices:
	print dev.name , dev.mac



hjeedom = httplib2.Http()
############### Parse device page
for key, (off, on, setip, name) in devicesMng.items():
	send = False
	listDevByName = [dev for dev in devices if dev.mac == key]
	if len(listDevByName) > 0:
		if key in devStatus:
			send = not devStatus[key][1]
		else:
			send = True
		devStatus[key] = (name, True)		
			
	else:
		if key in devStatus:
			send = devStatus[key][1]
			devStatus[key] = (name, False)
	############## Call jeedom command if required
	print send 
	if send & (key in devicesMng):
		CommandURL = jBaseURL + "&type=cmd&id=%d" % devicesMng[key][devStatus[key][1]]
		#print name, devicesMng[key][devStatus[key][1]]==on
		jresp, jcontent = hjeedom.request(CommandURL, "GET", body="foobar")
		print name, jresp['status'],CommandURL
		# update ip value
		if (len(listDevByName) > 0) & (setip > 0):
			CommandURL = jBaseURL + "&type=cmd&id=%d" % setip + "&title=&message=" + listDevByName[0].ip
			jresp, jcontent = hjeedom.request(CommandURL, "GET", body="foobar")
			print name, jresp['status'],CommandURL
#end for
			

			

		
	
############## Save current status to file	
with open(datafilename, 'w') as fp:
    json.dump(devStatus, fp)
