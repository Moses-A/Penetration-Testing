#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"
# This code requires the Anonymous.py File, so it may import everything

from Anonymous import *						
import optparse

ab = Anonymous(proxies=[], user_agents = [('User-agent', 'GoodIncognitoMode')])		# Grabs class and sets values to previously null values

def GetDifferentCookies(website):
	for attempt in range(1, 6):							# Sets a maximum of only six attempted cookie grabs
		ab.anonymize()								# Calls the anonymize function from the Anonymous python file
		f = open('CookieRetrieval.txt', 'a')					# Will write too and clear or create the CookieRetrieval.txt file
		f.write('\t[Attempt] Retrieving Cookies From ' + website + ' Page\n\n')	# Writes this introduction
		response = ab.open(website)  						# Waits for the response from the website, SYN, SYN-ACK, ACK
		for cookie in ab.cookie_jar:						# Will look for the cookie from that specific website
			f.write(str(cookie))						# Will write the cookie to the file


# The main function grabs the users information, and sends the information after the parser, to the GetDifferenCookies function, which then calls the Anonymous Class
def main():
	parser = optparse.OptionParser("Usages For Program -W <Website> Format: 'http://www.google.com' ")
	parser.add_option('-W', '--Website', dest='website', type='string', help='Specify Website To Gain Cookies From', default='http://www.google.com')
	(options, args) = parser.parse_args()
	website = options.website	
	if website == None:
		print parser.usage
		exit(0)
	f = open('CookieRetrieval.txt', 'w')					# Will write too and clear or create the CookieRetrieval.txt file
	GetDifferentCookies(website)							# Calls for the GetDifferentCookies function
	

if __name__ == '__main__':
	main()
