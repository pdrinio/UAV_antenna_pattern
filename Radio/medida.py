############################################################
# medida.py
# Programa main del modulo de medida de potencia.
# En este programa se crea una instancia a la clase radioDRON
# de GNURadio y se ejecuta, a la vez que se conecta al servidor
# en el localhost y le envia las medidas de potencia tomadas.
############################################################

import time
import socket
import sys
import struct
import math
import radioGRC
import getopt

#frequency = 868706250
frequency = 89500000
radio_server_host = "127.0.0.1"
radio_server_port = 6000
radio_server_params = (radio_server_host, radio_server_port)

# Create and start GNURadio task
print('Creating and starting a GNURadio task...')
try:
    GRC_task = radioGRC.radioGRC(89500000)
    GRC_task.start()
    time.sleep(1)
    print('GNURadio task created and started.')
except Error:
    print('Error creating/starting a GNURadio task.')

# Connect to radio_server
print('Connecting to radio_server...')
try:
    radio_server_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    radio_server_client.connect(radio_server_params)
    print('Connected to radio_server.')
except KeyboardInterrupt:
    print('Interrupted by user.')
    GRC_task.stop()
    GRC_task.wait()
    sys.exit(1)
except:
    print('Error connecting to radio_server.')
    GRC_task.stop()
    GRC_task.wait()
    sys.exit(1)

# Main loop
print('Measuring...')
while True:
    try:
        # Get value from GRC_task
        msg = struct.pack('f', GRC_task.get_var())
        # Send value to radio_server
        radio_server_client.send(msg)
        time.sleep(0.1)
    except KeyboardInterrupt:
        print ("Interrupted by user\n")
        radio_server_client.close()
        GRC_task.stop()
        GRC_task.wait()
    except:
        print('Error taking measurements.')
        radio_server_client.close()
        GRC_task.stop()
        GRC_task.wait()
        sys.exit(1)