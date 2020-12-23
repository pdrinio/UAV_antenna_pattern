############################################################
# servidor.py
# Este es el modulo de la clase Servidor que hereda de Thread. 
# Esta clase consiste en un servidor que se ejecuta en un hilo
# aparte y que lee la lectura de potencia obtenida por el 
# programa implementado en GNURadio.
############################################################

import socket
import math
import sys
import time
import struct
import threading

class Servidor_sdr (threading.Thread):
	# Variable miembro de la clase 
	# en la que se guarda la potencia leida.
	power = 0

	def __init__(self, dir_ip, puerto):
		threading.Thread.__init__(self)
		self.dir_servidor = (dir_ip, puerto)

	def receive(self):
		# En este metodo se lee lo que llegua del cliente,
		# y se guarda en la variable potencia como float.
		while 1:
			buf_rec = self.cliente.recv(4)
			fl = struct.unpack('f', buf_rec)
			self.power = fl[0]

	def run(self):
		# Metodo de inicio del servidor en un hilo aparte.
		# Este metodo es llamado al ejecutar el metodo start()
		self.sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sock_servidor.bind(self.dir_servidor)

		self.sock_servidor.listen(1)
		print ("servidor.run(): Escuchando.\n")

		self.cliente, addr = self.sock_servidor.accept()
		print ("servidor.run(): Aceptado.\n")

		self.recibe()

	def stop(self):
		# Se cierran las conexiones 
		# y se vuelve al hilo principal.
		self.cliente.close()
		self.sock_servidor.close()
		self.join()

	def get_power(self):
		return self.power