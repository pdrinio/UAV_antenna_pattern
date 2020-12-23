
import turntable
#import auxiliar
import servidor_sdr
import threading
#import simsdr
#from pymavlink import mavutil
import datetime
import time

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

#tcp:127.0.0.1:5763
    

turntable = turntable.Turntable() 
turntable.setparams(500,500) # maxspeed, maxaccel

servidor_sdr = servidor_sdr.Servidor_sdr("", 6000)
servidor_sdr.start()

#receiver = simsdr.SimSDR()

    
tinicio = datetime.datetime.now()
print('Init time: ', tinicio)

file = open("medidas.txt", "w")

line1 = []
size = 1000
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.zeros(len(x_vec))
#x_vec = np.zeros(1)
#y_vec = np.zeros(1)

turntable.start(360)
while 0!=1:
    #potencia = serv.get_potencia()
    #demora = auxiliar.obtener_demora(centro, dron.location.global_relative_frame)
    
    #potencia = receiver.prx(demora)
    power = servidor_sdr.get_power()
	#print ("Potencia: ", str("{0:.2f}".format(potencia)))
    y_vec[-1] = power
    line1 = live_plotter(x_vec,y_vec,line1)
    y_vec = np.append(y_vec[1:],0.0)

    #print ("Potencia: "+ str("{0:.2f}".format(potencia)) + " Demora: " + str("{0:.2f}".format(demora)) + "\n")
    #file.write(str("{0:.2f}".format(demora)) + "," + str("{0:.2f}".format(potencia)) + str("\n"))
    time.sleep(0.1)

tfin = datetime.datetime.now()
print('Hora de finalización vuelo circular: ', tfin)
print('Tiempo invertido: ', (tfin-tinicio).total_seconds())
file.close()
turntable.end()
servidor_sdr.stop()

