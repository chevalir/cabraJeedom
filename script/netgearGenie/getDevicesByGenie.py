#!/usr/bin/env python

import sys
import httplib2
import json
from pynetgear import Netgear
from collections import namedtuple



# devicesMng contains the list of devices managed in Jeedom
# the key could be the IP or the Mac adresse. The OFF and ON value are the 
# commands ID to set the state on or off.  
#   
#                Mac Adresse          OFF   ON       Name
devicesMng = {'B4:58:D5:52:36:0D' : (7739, 7738, 'Dev B')
         		, 'B8:37:0D:A2:03:5K' : (7744, 7743, 'Dev 3')
         		, 'K3:30:86:4B:29:44' : (7705, 7704, 'PC')
         		, 'A8:0A:D8:4B:D6:36' : (7706, 7700, 'iPhone')
         		, '44:56:B6:35:6B:A3' : (7765, 7764, 'IPad')
         		, '68:70:74:D9:83:B3' : (7766, 7760, 'Printer')
         		, '68:93:74:67:75:2B' : (7775, 7774, 'Tel A')
}

############## Init URL from arguments 
if len(sys.argv) < 6:
	print 'Not enougth args %d' % len(sys.argv)
	print 'syntax:getDevicesByGenie.py <Jeedom IP> <JeedomApiKey> <router login> <router pwd>'
	exit(1)
jIP = sys.argv[1]
jAPIKEY = sys.argv[2] # My Jeedom API Key
routerLogName = sys.argv[3] 
routerPWD = sys.argv[4]
routerIP = sys.argv[5]
jBaseURL = "http://" + jIP + "/core/api/jeeApi.php?apikey=" + jAPIKEY # My jeedom api base URL

############### load previous status from file ( if any )
datafilename = '/tmp/devStatuslist.json'
devStatus = {}
try :
	with open(datafilename, 'r') as fp:
		devStatus = json.load(fp)
except:
	print "first call"

# uncomment next line to force reset of list or delete manualy the file
#devStatus = {}



################ read device page and logout
#   Device = namedtuple("Device", ["signal","ip","name","mac","type","link_rate"])	


netgear = Netgear(routerPWD, routerIP, routerLogName, 80)
devices = netgear.get_attached_devices()

# uncomment next line to enable log
#print devices



hjeedom = httplib2.Http()
############### Parse device page
for key, (off, on, name) in devicesMng.items():
	send = False
	listDevByName = [dev for dev in devices if dev.mac == key]
	if len(listDevByName) > 0:
		if key in devStatus:
			send = not devStatus[key][1]
			devStatus[key] = (name, True)
		else:
			devStatus[key] = (name, True) 
			send = True
	else:
		if key in devStatus:
			send = devStatus[key][1]
			devStatus[key] = (name, False)
############## Call jeedom command if required
	if send & (key in devicesMng):
		CommandURL = jBaseURL + "&type=cmd&id=%d" % devicesMng[key][devStatus[key][1]]
		#print name, devicesMng[key][devStatus[key][1]]==on
		jresp, jcontent = hjeedom.request(CommandURL, "GET", body="foobar")
		print jresp['status'],CommandURL
		
	
############## Save current status to file	
with open(datafilename, 'w') as fp:
    json.dump(devStatus, fp)
