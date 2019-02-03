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
	#                     MacID  ( SetON, setOFF,  setIP   Name
devicesMng = {'90:9E:UI:8A:45:8O' : (5885, 5888, 5880,	'Print')
        		, '?????????????????' : (1111, 2222, 3333, 'deviceName')
        		
}

############## Init URL from arguments 
if len(sys.argv) < 6:
	print 'Not enougth args %d' % len(sys.argv)
	print 'syntax:updateIPStatus.py <Jeedom IP> <JeedomApiKey> <router login> <router pwd> <Router IP>'
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
		# CommandURL = jBaseURL + "&type=cmd&id=%d" % devicesMng[key][devStatus[key][1]]
		CommandURL = jBaseURL + "&type=cmd&id=%d" % devicesMng[key][False == devStatus[key][1]]
		jresp, jcontent = hjeedom.request(CommandURL, "GET", body="foobar")
		time.sleep(0.1)
		print name, jresp['status'],CommandURL
		# update ip value
		if (len(listDevByName) > 0) & (setip > 0):
			CommandURL = jBaseURL + "&type=cmd&id=%d" % setip + "&title=&message=" + listDevByName[0].ip
			jresp, jcontent = hjeedom.request(CommandURL, "GET", body="foobar")
			print name, jresp['status'],CommandURL
			time.sleep(0.1)

#end for
			

			

		
	
############## Save current status to file	
with open(datafilename, 'w') as fp:
    json.dump(devStatus, fp)
