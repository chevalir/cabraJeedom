#!/usr/bin/env python

##  You have to change :
##  <MyJeedomIP>   by the IP of your Jeedom
##  <MyRouterIP>   by the IP of your router
##  <BaseIpOfYourDevice>  by the base IP of your Devices with the last number ex : 168.192.5.
## V.2

import sys
import httplib2
import time
import re
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
	# devicesMng contains the list of devices managed in Jeedom
	# the key could be the IP or the Mac adresse. The OFF and ON value are the
	# commands ID the set the state on or off.
	#
	#                     MacID            ON  OFF   setIP   Name
	# https://www.fioulreduc.com/prix-fioul
	# http://192.168.1.7/core/api/jeeApi.php?apikey=gjdbk9ri4ea1ltwj2pj8&type=cmd&id=2348


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
	if len(sys.argv) < 3:
		print 'Not enougth args %d' % len(sys.argv)
		print 'syntax:updateIPStatus.py <Jeedom IP> <JeedomApiKey> <router login> <router pwd>'
		exit(1)
	jIP = sys.argv[1]
	jAPIKEY = sys.argv[2] # My Jeedom API Key
	jmyRegionID = int(sys.argv[3]) # refID of Region virtual info
	jIDVirtual = int(sys.argv[4]) # refID of Prix virtual command

	jBaseURL = "http://" + jIP + "/core/api/jeeApi.php?apikey=" + jAPIKEY # My jeedom api base URL
	
		## get region from Jeedom Virtual device
	CommandURL = jBaseURL + "&type=cmd&id=%d" % jmyRegionID
	content = requests.get(CommandURL)
	myRegion = content.text
	print myRegion
	
	siteURL = "https://www.fioulreduc.com/prix-fioul/%s" % myRegion
	
	############### load previous status from file ( if any )
	datafilename = '/tmp/prixfioul.json'
	devStatus = {}
	try :
		with open(datafilename, 'r') as fp:
			devStatus = json.load(fp)
	except:
		print "first call"
	# uncomment to force reset of list or delete manualy the file
	# devStatus = {}
	
	hjeedom = httplib2.Http(".cache")
	content = requests.get(siteURL)
	print ("done 1")
	## print ( content.text )
	soup =  BeautifulSoup(content.text, "html.parser")
	##print ( soup )
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
	dd = table_data[0][0]
	prixstr = table_data[0][1]
	## remove Euro charactere
	prixnum = ''.join(ch for ch in prixstr if ch.isdigit())	
	#print (table_data[0])
	#print (prixnum)
	

  ############## Call jeedom command if required
	# update ip value
	CommandURL = jBaseURL + "&type=cmd&id=%d" % jIDVirtual + "&slider=0," + prixnum
	#print (CommandURL)

	jresp, jcontent = hjeedom.request(CommandURL, "GET", body="foobar")
	#print (jresp)
	#end for
	


if __name__ == '__main__':
    status = main()
    sys.exit(status)