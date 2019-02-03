#!/usr/bin/env python

import sys
import httplib2
import json

# devicesMng contains the list of devices managed in Jeedom
# the key could be the IP or the Mac adresse. The OFF and ON value are the 
# commands ID the set the state on or off.  
#   
#              IP or MacID            OFF  ON       Name
devicesMng = {'B4:18:D1:12:C6:5D' : (2039, 2038, 'iPhone B')
         		, '192.168.1.12'      : (2044, 2043, 'iPod Touch')
         		, '192.168.1.17'      : (2051, 2050, 'iMac Wifi')
         		, 'A8:FA:D8:0B:D6:C6' : (2056, 2055, 'iPhone M')
         		, '00:16:B6:C1:6B:AC' : (2061, 2060, 'CabarWifi2')
         		, '68:7F:74:D9:8C:B3' : (2066, 2065, 'PAP Tel')
         		, '68:9C:70:67:71:2B' : (2071, 2070, 'iPad')
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
routerRootURL = "http://192.168.1.1/"  # My router baseURL
DevURL = "DEV_device.htm"      # page to list connected devices 
LogoutURL = "LGO_logout.htm"   # page to logout

############### load previous status from file ( if any )
datafilename = '/tmp/devStatuslist.json'
devStatus = {}
try :
		
	with open(datafilename, 'r') as fp:
		devStatus = json.load(fp)
except:
	print "first call"
# uncomment to force reset of list or delete manualy the file
# devStatus = {}



################ read device page and logout
hrouteur = httplib2.Http()
hjeedom = httplib2.Http()
hrouteur.add_credentials(routerLogName, routerPWD) # Basic authentication
#call device page, this page contains the list of device connected IP and Mac
resp, content = hrouteur.request(routerRootURL+DevURL, "GET", body="foobar")
if resp['status'] != '200':
	print 'Access error status:' + resp['status']
	exit(1)
#call Logout page
resp, contentOut = hrouteur.request(routerRootURL+LogoutURL, "GET", body="foobar")

############### Parse device page
for key, (off, on, name) in devicesMng.items():
	send = False
	index = content.find(key)
	if index > -1:
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
