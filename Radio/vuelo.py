###########################################################
# vuelo.py
# Programa main del modulo plataforma de vuelo.
# Este programa solicita datos al usuario de altura, radio y
# posicion. Despues en un hilo aparte se inicia un objeto de la 
# clase Servidor y se pone en escucha.
# Despues se crea una instancia de la clase 
# Multicoptero, se arma y se le ordena hacer el vuelo circular.
# En un bucle se recogen las medidas del Servidor y se escriben
# en un fichero junto a la demora respecto a la antena.
############################################################


# dronekit-sitl copter --model=quad --home=42.395969,-8.708963,0,0

from dronekit import *
import multicoptero
import auxiliar
import servidor
import threading
import simsdr
from pymavlink import mavutil
import datetime

import matplotlib.pyplot as plt
import numpy as np

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-',alpha=0.8)        
        #update plot label/title
        plt.ylabel('dB')
        plt.title('Received Power'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

altura = 10
radio = 100
lat = 42.395969
long = -8.708963
precision = 10
velocidad = 1

def set_roi(location, vehicle):
    # create the MAV_CMD_DO_SET_ROI command
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_DO_SET_ROI, #command
        0, #confirmation
        0, 0, 0, 0, #params 1-4
        location.lat,
        location.lon,
        location.alt
        )
    # send command to vehicle
    vehicle.send_mavlink(msg)
    
def condition_yaw(heading, vehicle, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)



#MAVProxy
dron = connect("udp:127.0.0.1:14540", wait_ready = True, vehicle_class = multicoptero.Multicoptero)

#tcp:127.0.0.1:5763

serv = servidor.Servidor("", 6000)
serv.start()

receiver = simsdr.SimSDR()

dron.takeoff(altura)

centro = LocationGlobalRelative(lat, long, altura)

demora = auxiliar.obtener_demora(centro, dron.location.global_relative_frame)

# Vuelo de aproximación al punto de inicio de medidas
dron.aprox_flight(centro, radio, altura, velocidad)

#condition_yaw(90, dron, True)

set_roi(centro, dron) # asi me aseguro que el dron siempre mira hacia la antena


# Vuelo circular con los siguientes parámetros:
# (centro, radio, altura, precision, velocidad, demora_inicial, sentido)
th_vuelo = threading.Thread(target=dron.circle_flight, args=(centro, radio, altura, precision, velocidad, demora, 1))
tinicio = datetime.datetime.now()
print('Hora de inicio vuelo circular: ', tinicio)
th_vuelo.start()

file = open("medidas.txt", "w")

line1 = []
size = 1000
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.zeros(len(x_vec))
#x_vec = np.zeros(1)
#y_vec = np.zeros(1)

while dron.end_flight == 0:
    #potencia = serv.get_potencia()
    demora = auxiliar.obtener_demora(centro, dron.location.global_relative_frame)
    
    potencia = receiver.prx(demora)
    y_vec[-1] = potencia
    line1 = live_plotter(x_vec,y_vec,line1)
    y_vec = np.append(y_vec[1:],0.0)

    #print ("Potencia: "+ str("{0:.2f}".format(potencia)) + " Demora: " + str("{0:.2f}".format(demora)) + "\n")
    file.write(str("{0:.2f}".format(demora)) + "," + str("{0:.2f}".format(potencia)) + str("\n"))
    time.sleep(0.1)

tfin = datetime.datetime.now()
print('Hora de finalización vuelo circular: ', tfin)
print('Tiempo invertido: ', (tfin-tinicio).total_seconds())
file.close()
serv.stop()
print ("mision cumplida, volvemos.\n")

dron.parameters['RTL_ALT'] = 0 # return at current altitude
dron.mode = VehicleMode('RTL')

dron.close()
dron.fin()
