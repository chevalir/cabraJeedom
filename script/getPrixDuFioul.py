#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def main():
	siteURL = "https://prixfioul.fr"
	tableID = u"Prix du fioul des régions"
	
	##myRegion = u"Prix du fioul en Poitou Charentes"
	
	############## Init URL from arguments
	if len(sys.argv) < 3:
		print 'Not enougth args %d' % len(sys.argv)
		print 'syntax:updateIPStatus.py <Jeedom IP> <JeedomApiKey> <router login> <router pwd>'
		exit(1)
	jIP = sys.argv[1] # Jeedom server IP
	jAPIKEY = sys.argv[2] # My Jeedom API Key
	jmyRegionID = int(sys.argv[3]) # refID of Region virtual info
	jIDVirtual = int(sys.argv[4]) # refID of Prix virtual command
	
	jBaseURL = "http://" + jIP + "/core/api/jeeApi.php?apikey=" + jAPIKEY # My jeedom api base URL
	
	## get region from Jeedom Virtual device
	CommandURL = jBaseURL + "&type=cmd&id=%d" % jmyRegionID
	content = requests.get(CommandURL)
	myRegion = content.text
	##print myRegion
	
	## Get table from prixFioul web site
	content = requests.get(siteURL)
	soup =  BeautifulSoup(content.text, "html.parser")

  ## Get table
	try:
			table = soup.find("table", summary=re.compile(tableID))
			## , summary=re.compile("Prix du fioul des r") 
	except AttributeError as e: 
			print 'No tables found, exiting'
			return 1
	# Get rows
	try:
			rows = table.find("tr" )
			while rows :
				rows = rows.find_next("tr")				
				if  myRegion in rows.find("th").get_text() :
					table_data = rows.find_next("td")
					prixstr = table_data.get_text()
					##print prixstr
	except AttributeError as e:
			rows = 0
	
	## remove Euro character
	prixnum = ''.join(ch for ch in prixstr if ch.isdigit())	
	print (prixnum)

  ############## Call jeedom command if required
	# update ip value
	CommandURL = jBaseURL + "&type=cmd&id=%d" % jIDVirtual + "&slider=0," + prixnum
	print (CommandURL)
	content = requests.get(CommandURL)

if __name__ == '__main__':
    status = main()
    sys.exit(status)