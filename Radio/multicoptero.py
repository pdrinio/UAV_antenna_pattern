############################################################
# multicoptero.py
# Este es el modulo de la clase Multicoptero
# que hereda de Vehicle. 
# Esta clase implementa metodos a un mas alto nivel para
# despegue, cambio de altura, movimiento a un punto
# y vuelo circular.
############################################################

import sys, time
import dronekit
from dronekit import *
import auxiliar

class Multicoptero (dronekit.Vehicle):
    # Variable que determina si se ha recibido COMMAND_ACK o no
    cmd_ack = 0
    end_flight=0

    def __init__(self, *args):
        # Se inicia desde la clase madre
        super(Multicoptero, self).__init__(*args)
        # Cuando se reciba el mensaje COMMAND_ACK se ejecuta el metodo ack
        self.add_message_listener("COMMAND_ACK", self.ack)

    def ack(self, name, msg, otr):
        #Cuando se recibe el mensaje COMMAND_ACK, la variable cmd_ack pasa a valer 1, en caso contrario deberia valer 0, esto se implementara en cada metodo segun sea necesario
        self.cmd_ack = 1

    
    def circulo(self, radius, rate):
       
        self.parameters["CIRCLE_RADIUS"] = radius # 0 to 10000	centimeters, increment: 100 cm
        self.parameters["CIRCLE_RATE"] = rate     # -90 to -90	degrees per second, increment: 1 deg/s
        print ("circulo(): Modo CIRCLE...")
        self.mode = VehicleMode("CIRCLE")
            
    
    def takeoff(self, altura):
        #Este metodo ejecuta el armado y despegue del dron hasta la altura argumento

        #Comprobacion de si es armable o no
        print ("despegue(): Comprobaciones previas al despegue.\n")
        while not self.is_armable == True:
            time.sleep(2)
            print ("despegue(): Multicoptero no se puede armar.\n")

        #Armado de vehiculo
        print ("despegue(): Armando vehiculo...\n")
        self.mode = VehicleMode("GUIDED")
        self.armed = True
        while not self.mode.name == "GUIDED" and not self.armed == True:
            time.sleep(2)
            print ("despegue(): Me estoy armando...\n")
        print ("despegue(): Vehiculo armado.\n")

        #Orden de despegue, a continuacion en un bucle se comprueba cada segundo si se ha alcanzado la altura ordenada
        print ("despegue(): Despegando...\n")
        self.simple_takeoff(altura)
        while True:
            time.sleep(1)
            #print ("despegue(): Altura: " +str(self.location.global_relative_frame.alt)+ "\n")
            if self.location.global_relative_frame.alt>=altura*0.95:
                print ("despegue(): Alcanzada altura de: " + str(self.location.global_relative_frame.alt) + "\n")
        #Una vez alcanzada la altura, se devuelve 0 representando despegue exitoso
                return 0

    def goto(self, destino, velocidad):
        #Metodo que ordena al dron dirigirse a un punto a una velocidad determinada. El dron debe estar en modo GUIDED de antes.

        #self.mode = VehicleMode("GUIDED")
        #La variable de clase cmd_ack se pone a 0 para comprobar si las ordenes llegan al dron
        self.cmd_ack = 0

        #Se ordena al dron dirigirse a la posicion destino, a continuacion se comprueba si la orden ha llegado o no con cmd_ack, en caso de que no llegue, se vuelve a enviar una vez, si tampoco llega, la funcion devuelve 1 indicando error
        #print ("goto(): Dirigiendome hacia: " + str(destino) + "\n")
        distoriginal = auxiliar.obtener_distancia(self.location.global_relative_frame, destino)
        self.simple_goto(destino, airspeed=velocidad)
        time.sleep(2)
        if not self.cmd_ack == 1:
            print ("goto(): No se envio la orden. Reenviando...\n")
            #Tiempo de espera antes de volver a enviar la orden
            time.sleep(5)
            self.simple_goto(destino, airspeed=velocidad)
            time.sleep(2)
            if not self.cmd_ack == 1:
                print ("goto(): No es posible enviar la orden al dron.\n")
                return 1

        #Una vez la orden ha llegado, en un bucle se comprueba cada 2 segundos si la aeronave ha llegado ya a su destino, con una precision de 0.5 metros. Una vez alcanzado se devuelve 0 indicando exito
        while self.mode.name == "GUIDED":
            dist = auxiliar.obtener_distancia(self.location.global_relative_frame, destino)
            if dist <= 2:
                #print ("goto(): He llegado a mi destino.\n")
                return 0
            #print ("goto(): En vuelo, quedan " + str(auxiliar.obtener_distancia(self.location.global_relative_frame, destino)) +" m\n")
            time.sleep(2)

        #En caso de que no se llegue al destino, se devuelve 1 indicando que hubo algun problema
        print ("goto(): Hubo algun problema, no se ha alcanzado el destino.\n")
        return 1

    def cambiar_altura(self, altura, velocidad):
        #Este metodo sirve para cambiar la altura en una posicion estatica. Funciona de manera muy similar a goto() con comprobacion de COMMAND_CHECK
        #self.mode = VehicleMode("GUIDED")
        posicion_nueva = self.location.global_relative_frame
        posicion_nueva.alt = altura
        self.cmd_ack = 0

        print ("cambiar_altura(): Cambiando cota a "+str(altura)+" m a una velocidad vertical de "+str(velocidad)+" m/s.\n")
        self.simple_goto(posicion_nueva, airspeed=velocidad)
        time.sleep(2)
        if not self.cmd_ack == 1:
            print ("goto(): No se envio la orden. Reenviando...\n")
            #Tiempo de espera antes de volver a enviar la orden
            time.sleep(2)
            self.simple_goto(posicion_nueva, airspeed=velocidad)
            time.sleep(2)
            if not self.cmd_ack == 1:
                print ("goto(): No es posible enviar la orden al dron.\n")
                return 1

        while self.mode.name == "GUIDED":
            time.sleep(1)
            print ("cambiar_altura(): Altura: " +str(self.location.global_relative_frame.alt) + "\n")
            if math.fabs(self.location.global_relative_frame.alt-altura)<=altura*0.05:
                print ("cambiar_altura(): Alcanzada altura de: " + str(self.location.global_relative_frame.alt) + "\n")
            #Una vez alcanzada la altura, se devuelve 0 representando despegue exitoso
                self.end_flight = 1
                return 0

    def circle_flight(self, centro, radio, altura, precision, velocidad, demora_inicial, sentido):
        #Este metodo ordena al dron realizar un vuelo circular alrededor del punto centro con un radio y a una velocidad dadas. La precision indica los grados que abarcara cada lado que tendra el poligono asemejable a la circunferencia. La demora inicial indica el angulo inicial respecto al norte del primer punto del poligono, y el sentido 1 si es horario, -1 antihorario

        self.mode = VehicleMode("GUIDED")
        self.end_flight = 0
        print ("vuelo_circular(): Realizando vuelo circular.\n")
        for i in range((360//precision)+1):
            p1 = auxiliar.obtener_punto_demdist(centro, radio, demora_inicial+sentido*i*precision, altura)
            print ("vuelo_circular(): Waypoint: " + str(i) + "\n")
            if self.goto(p1, velocidad)==1:
                print ("vuelo_circular(): Hay un problema desconocido, no se pudo alcanzar el siguiente waypoint.\n")
                return 1
        print ("vuelo_circular(): Realizado vuelo circular con exito.\n")
        self.end_flight = 1
        return 0

    def aprox_flight(self, centro, dist_min, altura, velocidad):
        posicion_original = self.location.global_relative_frame
        demora = auxiliar.obtener_demora(centro, posicion_original)
        punto_minimo = auxiliar.obtener_punto_demdist(centro, dist_min, demora, altura)

        print ("vuelo_aproximacion(): Iniciando vuelo de aproximacion hasta punto situado a " +str(dist_min)+" del centro.\n")
        self.goto(punto_minimo, velocidad)
        return 0


    def fin(self):
        #self.flush()
        self.close()