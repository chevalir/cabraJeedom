#!/usr/bin/env python

##  You have to change :
##  <MyJeedomIP>   by the IP of your Jeedom 
##  <MyRouterIP>   by the IP of your router
##  <BaseIpOfYourDevice>  by the base IP of your Devices with the last number ex : 168.192.5.


import httplib2
import json
#          IP     ON    OFF
listid = { 24 : (2040, 2039), # iPhone B
           12 : (2044, 2043)  # iPod T
}



ipStatus = {}
try :
	with open('iplist.json', 'r') as fp:
		ipStatus = json.load(fp)
except:
	print ""
#ipStatus = {}

	
	
#prevlist = list(ipStatus)

#print ipStatus
DevURL = "http://<MyRouterIP>/DEV_device.htm"
hrouteur = httplib2.Http(".cache")
hjeedom = httplib2.Http(".cache")

hrouteur.add_credentials('login', 'password') # Basic authentication set YOUR login password 

resp, content = hrouteur.request(DevURL, "GET", body="foobar")

send = False;

for num in range(1,120):        #to iterate between 10 to 20
	send = False
	ip = "<BaseIpOfYourDevice>"+"%d" % num   # change the base IP Addresse ex 192.168.3.
	index = content.find(ip)
	if index > -1:
		if ip in ipStatus:
			send = ipStatus[ip] == False
			ipStatus[ip] = True
		else:
			ipStatus[ip] = True 
			send = True
	else:
		if ip in ipStatus:
			send = ipStatus[ip] == True
			ipStatus[ip] = False
			
	if send & (num in listid):
		#ipStatus[ip] = ipStatus[ip] == 0 # to reverse the status
		print ip + " status:%d " % ipStatus[ip] 
		print listid[num][ipStatus[ip]]
		ONURL  = "http://<MyJeedomIP>/core/api/jeeApi.php?apikey=gjdbk9ri4ea1ltwj2pj8&type=cmd&id=%d" % listid[num][ipStatus[ip]]
		jresp, jcontent = hjeedom.request(ONURL, "GET", body="foobar")
		

print ipStatus
	
with open('iplist.json', 'w') as fp:
    json.dump(ipStatus, fp)