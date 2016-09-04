#!/usr/bin/env python2
# written by Moses Arocha
# Written with the help of TJ O'Connor in his book "Violent Python"


import mechanize
import cookielib
import random


class Anonymous(mechanize.Browser):
    def __init__(self, proxies = [], user_agents = []):
	mechanize.Browser.__init__(self)
	self.set_handle_robots(False)
	self.proxies = proxies
	self.user_agents = user_agents + ['Microsoft/8.0 ', 'Internet Explorer/11.01', 'ExactSearch', 'Nokia7110/1.0']	
	self.cookie_jar = cookielib.LWPCookieJar()
	self.set_cookiejar(self.cookie_jar)
        self.anonymize()						
	
    def clear_cookies(self):
	self.cookie_jar = cookielib.LWPCookieJar()
	self.set_cookiejar(self.cookie_jar)
	
# The information about your computer that will be sent, make sure this is not correct!!
    def alter_user_agent(self):
	index = random.randrange(0, len(self.user_agents))
	self.addheaders = [('User-agent', (self.user_agents[index]))]
	
    def alter_proxy(self):
	if self.proxies:
	    index = random.randrange(0, len(self.proxies))
	    self.set_proxies({'http': self.proxies[index]})

    def anonymize(self, sleep = False):			# This function will be called by the GetDifferentCookies function.
        self.clear_cookies()				# It will then reference and call the clear_cookies function and will run it on the localhost.
	self.alter_user_agent()				# It will then reference the alteruseragent function, and will begin the process of altering the information that will be sent to the website.
	self.alter_proxy()				# This will randomize the proxy information so that different cookies can be receieved.
	if sleep:
	    time.sleep(90)
