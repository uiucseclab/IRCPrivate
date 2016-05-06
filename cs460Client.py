#This irc client connects to a server using ssl encryption 

import socket
import ssl
import sys
import string



# --------------------------------------------- Initial Socket Setup -----------------------------------------------------------
nickname = 'cs460' #define nickname
server = "127.0.0.1" #Define IRC server
port = 6697 #Define IRC Server Port
chan = "#test" #Define initial channel to connect to

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define  IRC Socket
print "connecting to:" + server #print server to console
irc.connect((server,port)) #Connect to Server

ircSSL = ssl.wrap_socket(irc, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED) #wrap current socket with ssl using selfsigned cert

#---------------------------------------------Helper Functions -----------------------------------------------------------------
def sendPong(pingMessage):
	print "sending Pong"
	ircSSL.send('PONG ' + pingMessage + '\r\n')

def sendJoin(joinChannel):
	print channel
	ircSSL.send('JOIN ' + joinChannel + '\r\n') 

def sendPart(partChannel):
	print channel
	ircSSL.send('PART ' + partChannel + '\r\n') 

def sendMe(handWave):
	print handWave
	ircSSL.send('PRIVMSG ' + chan + ' :' + handWave + '\r\n')

def sendMessage(messageToSend):
	msg = messageToSend	
	ircSSL.send('PRIVMSG ' + chan + ' :' + messageToSend +'\r\n')


#----------------------------------------------Setup the user and join initial channel------------------------------------------ 
#receive initial data 
ircSSL.recv (4096) 

#Send the nickname 
ircSSL.send('NICK ' + nickname + '\r\n') 
#Send USER to server
ircSSL.send('USER cs460 cs460 cs460 :cs460 IRC\r\n') 
# Join a pre defined channel
ircSSL.send('JOIN ' + chan + '\r\n') 
#Send a Message to the channel
ircSSL.send('PRIVMSG ' + chan + ' :Hello people.\r\n') 


#---------------------------------------------Loop to continue receiving and sending messages-----------------------------------
while True: #Keep connection open
	data = str(ircSSL.recv (1024)) #Make Data the Receive Buffer

	print data #print buffer to console
	

	message = raw_input('INPUT $$$: ')  #collect input from user
	
	#Functionality to join a different channel with the form ("/join #<channel name>")
	#Check console input
	if "/join" in message:
		channel = message[6:]
		sendJoin(channel)

		

	#Functionality to part a channel with the form ("/part #<channel name>")
	#Check console input	
	if "/part" in message:
		channel = message[6:]
		chan = channel
		sendPart(channel)

	
	#Functionality to display the users nickname
	#Check console input
	if "/author" in message:
		author = nickname + "waves hello"
		sendMe(author)

	
	#Functionality to allow the client to exit out without having to use Ctrl-C
	#Check console input
	if "/exit" in message:
		exit()

	#Functionality to allow sending a message back to the server. Messages must be alternating between this client and another user
	#Check console input
	if "/message" in message:
		privmsg = message[9:]
		sendMessage(privmsg)

	
	
	#Check incoming data if being ping'd by other users	
	if data.find('PING') != -1: 
		sendPong(data.split()[1])




