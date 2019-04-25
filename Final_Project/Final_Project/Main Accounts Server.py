################################################
##                                            ##                                                      
##                  Imports                   ##                                                
##                                            ##                                                      
################################################
from helping_classes import TrackServerActivity
from threading import Thread
from select import select
import socket

################################################
##                                            ##                                                      
##            Server by Class                 ##                                                
##                                            ##                                                      
################################################
class MainServer():
	"""
	This class handles signing in, usernames, passwords
	and everything else related to the accounts of 
	customers.
	"""
	def __init__(self): 
		"""
		Initiates a 'MainServer' object and sets all 
		class parameters.
		"""
		self.accounts = {}
		# :type : dict{ string (username) : list[string (password), socket (computer socket), socket (phone socket) / None, ]}
		self.accounts_counter = 0
		# :type : int

		self.tracker = TrackServerActivity()
		# :type : TrackServerActivity

		self.server = socket.socket()
		# :type : socket
		self.IP = '0.0.0.0'
		# :type : string
		self.PORT = 8001
		# :type : int
		self.binded = False
		# :type : bool

	##################################
	##                              ##
	##   Users related functions    ##
	##                              ##
	##################################

	def username_taken(self, username): #Returns whether 'username' is taken.
		return username in self.accounts.keys()

	def password_taken(self, password): #Returns whether 'password' is taken.
		taken_passwords = []
		for item in self.accounts.values():
			taken_passwords.append(item[0])

		return password in taken_passwords

	#########################################################################################

	def sign_new_account(self, username, password, new_account_socket): #Signing in a new account. False if password or username is taken, True if account created.
		if self.username_taken(username) or self.password_taken(password):
			return False

		self.accounts[username] = (password, new_account_socket)
		self.accounts_counter = self.accounts_counter + 1
		self.tracker.update_history("NEW", username, None)
		return True

	def delete_account(self, username): #Deleting an existing account.
		if self.username_taken(username):
			del self.accounts[username]
			self.accounts_counter = self.accounts_counter - 1
			self.tracker.update_history("DEL", username, None)
			return True

		return False

	def approve_entrance(self, username, password): #Approving or declining a try to enter an account.
		if self.username_taken(username):
			if password == self.accounts[username][0]:
				self.tracker.update_history("LOGIN", username, None)
				return True

		return False

	#########################################################################################

	def change_username(self, username, new_username): #Changing an account's username.
		if not self.username_taken(new_username):
			self.accounts[new_username] = self.accounts[username]
			del self.accounts[username]
			self.tracker.update_history("USERNAME", username, new_username)
			return True

		return False

	def change_password(self, username, new_password): #Changing an account's password.
		if not self.password_taken(new_password):
			user_socket = self.accounts[username][1]
			self.accounts[username] = (new_password, user_socket)
			self.tracker.update_history("PASSWORD", username, password)
			return True 

		return False

	##################################
	##                              ##
	## Connection related functions ##
	##                              ##
	##################################

	def handle_requests(self, clientSocket): #Handles each socket request seperately, returns an answer and closes the socket.
		message = clientSocket.recv(2048) #Message: "request/username/..."
		request = message.split('/')

		if request[0] == "sgnwacc": #Message: "sgnwacc/username/password"
			answer = self.sign_new_account(request[1], request[2], clientSocket)
			clientSocket.send(answer)
			if not answer:
				clientSocket.close()

		elif request[0] == "delacc": #Message: "delacc/username"
			answer = self.delete_account(request[1])
			clientSocket.send(answer)
			if answer:
				clientSocket.close()

		elif request[0] == "appent": #Message: "appent/username/password"
			answer = self.approve_entrance(request[1], request[2])
			clientSocket.send(answer)

		elif request[0] == "chuser": #Message: "chuser/username/new username"
			answer = self.change_username(request[1], request[2])
			clientSocket.send(answer)

		elif request[0] == "chpass": #Message: "chpass/username/new password"
			answer = self.change_password(request[1], request[2])
			clientSocket.send(answer)

		else:
			clientSocket.send("ERROR")

	#########################################################################################

	def binding(self): #Binding the server and initialize it.
		while not self.binded:
    		try:
        		self.server.bind((self.IP, self.PORT))
        		self.binded = True
    		except:
       			self.PORT = self.PORT + 1

       	self.tracker.PORT = self.PORT

    ##################################
	##                              ##
	##        Run function          ##
	##                              ##
	##################################

    def run(self): #The actual running form of the server.
    	self.tracker.start()
    	self.binding()
    	while True:
    		self.server.listen(300)
    		(readables, writables, exceptional) = select([self.server] + [item[1] for item in self.accounts.values()], [item[1] for item in self.accounts.values()], [])
    		for s in readables:
        		if s is self.server:
            		(clientSocket , clientAddress) = s.accept()
            		Thread(target = self.handle_requests , args=(clientSocket, )).start()
            	else:
            		Thread(target = self.handle_requests , args=(s, )).start()

################################################
##                                            ##                                                      
##               Main                         ##                                                
##                                            ##                                                      
################################################
MainServerPClone = MainServer()
MainServerPClone.run()







