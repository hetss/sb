import socket
import time
import re
import sb

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "twitchname"
PASS = "oauthtoken"
CHAN = "#saltybet"
CHAT_MSG=r":(?P<username>\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(?P<message>.+)\r\n$"

connected = False
failures = 0
disconnect = 0
saltybet = sb.saltyBet()

try:
	while True:
		try:
			s=socket.socket()
			s.settimeout(300) # If no activity for 5 minutes, time out
			s.connect((HOST,PORT))
			s.send("PASS %s\r\n" % PASS)
			s.send("NICK %s\r\n" % NICK)
			s.send("JOIN %s\r\n" % CHAN)
			connected = True
		except socket.error as sockerr:
			print("Connection failed ("+str(sockerr.errno)+")")
			connected = False
			failures += 1
		if(connected):
			print("Connected")
			failures = 0
		while connected:
			try:
				response = s.recv(1024).decode("utf-8")
				if(len(response) == 0):
					disconnect = min(300, disconnect+1)
					print("Disconnected (Waiting "+str(disconnect)+" seconds)")
					connected = False
					s.shutdown(socket.SHUT_RDWR)
					s.close()
					break
				elif response == "PING :tmi.twitch.tv\r\n":
					s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
				else:
					r = re.match(CHAT_MSG,response)
					if(r != None):
						disconnect = max(0, disconnect-1)
						username = r.group('username')
						message = r.group('message')
						if(username.lower() == "waifu4u"):
							saltybet.parse(message)
			except socket.error as sockerr:
				print("Error: "+repr(sockerr))
				connected = False
				s.shutdown(socket.SHUT_RDWR)
				s.close()
			except UnicodeDecodeError:
				pass
		time.sleep(min(300,(failures*5+disconnect)))
except KeyboardInterrupt:
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	print("Interrupted. Socket closed.")
