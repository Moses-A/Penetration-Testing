#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"

# Attention:This code requires the Anonymous.py File, so it may import everything


from Anonymous import Anonymous						
import optparse


ab = Anonymous(proxies=[], user_agents = [('User-agent', 'GoodIncognitoMode')])		# Grabs class and sets values to previously null values


def GetDifferentCookies(website):
    for attempt in range(1, 6):							
        ab.anonymize()								
	f = open('CookieRetrieval.txt', 'a')					
	f.write('\t[Attempt] Retrieving Cookies From ' + website + ' Page\n\n')		# Writes this as introduction for ease. Not required.
	response = ab.open(website)  							# Waits for the response from the website, SYN, SYN-ACK, ACK
	for cookie in ab.cookie_jar:							# Will look for the cookie from that specific website and writes it to a file.
	    f.write(str(cookie))						


def main():
    parser = optparse.OptionParser("Usages For Program -W <Website> Format: 'http://www.google.com' ")
    parser.add_option('-W', '--Website', dest='website', type='string', help='Specify Website To Gain Cookies From', default='http://www.google.com')
    (options, args) = parser.parse_args()
    website = options.website	
    if website == None:
	print parser.usage
	exit(0)
    f = open('CookieRetrieval.txt', 'w')					
    GetDifferentCookies(website)				# Important: must be last so that all error handling can take place.
	

if __name__ == '__main__':
    main()
