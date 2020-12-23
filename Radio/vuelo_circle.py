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

altura = 10 # m
radio = 50  # m
lat = 42.395969
long = -8.708963
velocidad = 2 # m/s

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
dron = connect("tcp:127.0.0.1:5763", wait_ready = True, vehicle_class = multicoptero.Multicoptero)

serv = servidor.Servidor("", 6000)
serv.start()

receiver = simsdr.SimSDR()

dron.takeoff(altura)

centro = LocationGlobalRelative(lat, long, altura)

# Vuelo de aproximación al punto de inicio de medidas
dron.aprox_flight(centro, radio, altura, velocidad)

dron.parameters['WPNAV_ACCEL']=500

omega=velocidad*360/2/math.pi/radio #velocidad angular en deg/s
dron.circulo(radio*100, 1)

file = open("medidas.txt", "w")

while dron.end_flight == 0:
    #potencia = serv.get_potencia()
    demora = auxiliar.obtener_demora(centro, dron.location.global_relative_frame)
    
    potencia = receiver.prx(demora)


    #print ("Potencia: "+ str("{0:.2f}".format(potencia)) + " Demora: " + str("{0:.2f}".format(demora)) + "\n")
    file.write(str("{0:.2f}".format(demora)) + "," + str("{0:.2f}".format(potencia)) + str("\n"))
    time.sleep(0.1)


time.sleep(60)

file.close()
serv.stop()

print ("mision cumplida, volvemos.\n")
dron.parameters['RTL_ALT'] = 0 # return at current altitude
dron.mode = VehicleMode("RTL")


dron.close()
dron.fin()
