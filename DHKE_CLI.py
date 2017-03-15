#!/usr/bin/python
import socket
from random import randint
import re
import random

#Diffie-Hellman key exchange initializer - client side

class DHE:
	def __init__(self,root,prime,recv_key):
		self.root=root
#		print("Root: -->"+str(self.rp_val))
		self.prime=prime
#		print("Prime: -->"+str(self.root_prime[self.rp_val]))
		#return self.root , self.prime
		self.recv_key=recv_key
	def key_gen(self):
		range_start = 10**(7-1)
		range_end = (10**7)-1
		self.key = randint(range_start, range_end)
	def shared_key(self):
		mod=(self.root**self.key) % self.prime
		#print("Shared Key:"+ str(mod))
		return str(mod)
# To be built
	def secret_key(self):
		sec_key=(self.recv_key**self.key) % self.prime
		return sec_key

		
def DHKE_CLI(server_ip,client_ip,port_no):
	host = server_ip
	port = 8844
	IP=client_ip
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server
	server_address = (host, port)
	kfile=open('agent.key','w')
	print "Connecting to %s port %s" % server_address
	sock.connect(server_address)
	try:
		print "Starting negotiation with Diffie-Hellman key exchange server: "+str(server_ip)
		message="START_NEGOTIATION-"+str(IP)
		msg= message.encode('base64','strict')
		sock.send(msg)
		data=sock.recv(4096)
		if data:
			dataDecode=data.decode('base64')
			pattern=re.search(r"(\d+):(\d+):(\d+)-(\d+\.\d+\.\d+\.\d+)",dataDecode)
			if pattern:
				root=int(pattern.group(1))
				prime=int(pattern.group(2))
				recv_key=int(pattern.group(3))
				DHO=DHE(root,prime,recv_key)
				DHO.key_gen()
				share_key=DHO.shared_key()
				message1="SHARED_KEY-"+IP+"-"+share_key
				msg1=message1.encode('base64','strict')
				sock.send(msg1)
				key=DHO.secret_key()
				write_key=pow(root,key)
				print("Secret Key: " + str(write_key))
				kfile.write(IP+':'+str(write_key).encode('base64','strict'))
				kfile.close()
	#except socket.errno, e:
	#	print "Socket error: %s" %str(e)
	except Exception, e:
		print "Other exception: %s" %str(e)
	finally:
		print "Closing connection to the server"
		sock.close()

if __name__=='__main__':
	DHKE_CLI('127.0.0.1','192.168.1.3',8844)



