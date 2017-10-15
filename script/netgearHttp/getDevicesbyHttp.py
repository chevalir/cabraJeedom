#!/usr/bin/env python

##  You have to change :
##  <MyJeedomIP>   by the IP of your Jeedom
##  <MyRouterIP>   by the IP of your router
##  <BaseIpOfYourDevice>  by the base IP of your Devices with the last number ex : 168.192.5.

import sys
import httplib2
import time
import json
from bs4 import BeautifulSoup
from collections import namedtuple

# devicesMng contains the list of devices managed in Jeedom
# the key could be the IP or the Mac adresse. The OFF and ON value are the
# commands ID the set the state on or off.
#
#                     MacID            ON  OFF   setIP   Name
devicesMng = {'B4:88:P8:85:O6:5P' : (8809, 8808, 8884, 	'iPhone')
         		, 'B8:O7:5P:A5:5O:8E' : (8844, 8840, 8880, 	'iPod')
         		, '80:PP:B8:B4:48:9O' : (5805, 5804, 5806,	'iMac')
        		, '5O:9E:XO:8A:OA:8O' : (5878, 5877, 5879,	'PC')
}
	
def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
        table_data = row.find_all('td')
        if table_data:
            results.append([data.get_text() for data in table_data])
    return results

def is_number(s):
	try:
			float(s)
			return True
	except ValueError:
			pass
	
	try:
			import unicodedata
			unicodedata.numeric(s)
			return True
	except (TypeError, ValueError):
			pass
	return False

def main():
	
	############## Init URL from arguments
	if len(sys.argv) < 6:
		print 'Not enougth args %d' % len(sys.argv)
		print 'syntax:updateIPStatus.py <Jeedom IP> <JeedomApiKey> <router login> <router pwd>'
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
	# devStatus = {}
	
	devicesListURL = "http://"+routerIP+"/DEV_device.htm"
	hrouteur = httplib2.Http(".cache")
	hjeedom = httplib2.Http(".cache")
	hrouteur.add_credentials(routerLogName, routerPWD) # Basic authentication set YOUR login password
	resp, content = hrouteur.request(devicesListURL, "GET", body="foobar")
	## Call logoff
	devicesListURL = "http://"+routerIP+"/LGO_logout.htm"
	resp, contentlogoff = hrouteur.request(devicesListURL, "GET", body="foobar")
	print ( resp, contentlogoff )
	soup =  BeautifulSoup(content, "html.parser")

	# Get table
	try:
			table = soup.find('table')
	except AttributeError as e:
			print 'No tables found, exiting'
			return 1

	# Get rows
	try:
			rows = table.find_all('tr')
	except AttributeError as e:
			print 'No table rows found, exiting'
			return 1

	# Get data
	table_data = parse_rows(rows)
	connectedDev = []
	Devices = namedtuple("Devices", ["ip","name","mac"])
	for row in rows:
		table_data = row.find_all('td')
		if table_data:
			tdor = [data.get_text() for data in table_data]
			if is_number(tdor[0]):
				# print tdor[1]+' '+tdor[2]+' '+tdor[3]
				#  connectedDev.append({'ip':tdor[1],'name': tdor[2], 'mac': tdor[3]})
				pp = Devices(ip=tdor[1], name=tdor[2], mac=tdor[3] )
				connectedDev.append(pp)
	#print connectedDev
	print 'done'
	
	send = False;
	for key, (off, on, setip, name) in devicesMng.items():
		send = True
		listDevByName = [dev for dev in connectedDev if dev.mac == key]
		# print dev.mac,dev.name, key
		if len(listDevByName) > 0:
			if key in devStatus:
				send = not devStatus[key][1]
			else:
				send = True
			devStatus[key] = (name, True)		
			print ("listDevByName > 0")	
		else:
			if key in devStatus:
				send = devStatus[key][1]
			devStatus[key] = (name, False)
		############## Call jeedom command if required
		#print send 
		if send & (key in devicesMng):
			CommandURL = jBaseURL + "&type=cmd&id=%d" % devicesMng[key][False == devStatus[key][1]]
			#print name, devicesMng[key][False == devStatus[key][1]]
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
	#print devStatus
	with open(datafilename, 'w') as fp:
			json.dump(devStatus, fp)


if __name__ == '__main__':
    status = main()
    sys.exit(status)