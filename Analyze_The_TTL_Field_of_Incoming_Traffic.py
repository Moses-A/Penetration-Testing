#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"


from scapy.all import *
import os


def CaptureTraffic(packets):
    try:
        if packets.haslayer(IP):
	    ipsrc = packets.getlayer(IP).src
	    ipdst = packets.getlayer(IP).dst
	    ttl = str(packets.ttl)
 	    f = open('TTLField.txt', 'a')
	    f.write('\n [Source] Packet Received From: '+ipsrc+' with TTL Of: '+ttl)
	    f.write('\n\t  [Destination] Packet Received From: ' + ipdst + ' with TTL Of: '+ ttl)
    except:
	pass


def main():
    if not os.geteuid() == 0:
        sys.exit('\tMust Be Root!')
    f = open('TTLField.txt', 'w')
    os.system('chmod 777 TTLField.txt')
    f.write('\t Packet Capturing While Analyzing TTL Fields\n\n')
    sniff(prn=CaptureTraffic, store=0)

if __name__ == '__main__':
    main()
