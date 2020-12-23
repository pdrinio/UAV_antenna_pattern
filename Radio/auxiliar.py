############################################################
# auxiliar.py
# En este modulo hay una serie de funciones auxiliares que 
# permiten operaciones geometricas como obtener distancia
# u obtener demora entre dos puntos dados.
# Codigos obtenidos en su mayoria de ArduPilot
############################################################

import math
from dronekit import *

def obtener_distancia(punto1, punto2):
	"""
	Returns the ground distance in metres between two `LocationGlobal` or `LocationGlobalRelative` objects.
	This method is an approximation, and will not be accurate over large distances and close to the earth's poles. It comes from the ArduPilot test code:
https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
	"""
	dlat = punto2.lat - punto1.lat
	dlong = punto2.lon - punto1.lon
	return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def obtener_demora(punto1, punto2):
	"""
	Returns the bearing between the two LocationGlobal objects passed as parameters.
	This method is an approximation, and may not be accurate over large distances and close to the earth's poles. It comes from the ArduPilot test code: 
https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
	"""
	off_x = (punto2.lon - punto1.lon)*math.cos(math.pi*((punto1.lat+punto2.lat)/2)/180)
	off_y = punto2.lat - punto1.lat
	demora = math.atan2(off_x, off_y) * 57.2957795
	if demora < 0:
		demora += 360.00
	return demora

def obtener_punto_distancias(original_location, dNorth, dEast, altura):
	"""
	Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the specified `original_location`. The returned LocationGlobal has the same `alt` value as `original_location`.
	The function is useful when you want to move the vehicle around specifying locations relative to the current vehicle position.
	The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
	For more information see:
	http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
	"""
	earth_radius = 6378137.0 #Radius of "spherical" earth
	#Coordinate offsets in radians
	dLat = dNorth/earth_radius
	dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

	#New position in decimal degrees
	newlat = original_location.lat + (dLat * 180/math.pi)
	newlon = original_location.lon + (dLon * 180/math.pi)
	if type(original_location) is LocationGlobal:
		targetlocation=LocationGlobal(newlat, newlon, altura)
	elif type(original_location) is LocationGlobalRelative:
		targetlocation=LocationGlobalRelative(newlat, newlon, altura) 
	return targetlocation

def obtener_punto_demdist(original_location, distancia, demora, altura):
	"""
	Basado en la funcion obtener_punto_distancias() pero dando demora y distancia relativas a posicion central. Angulo de la demora empieza a contar el cero en el norte y aumenta en sentido horario igual que las demoras en los buques.
	"""
	dNorth = distancia*math.cos((demora*math.pi)/180)
	dEast = distancia*math.sin((demora*math.pi)/180)
	earth_radius = 6378137.0 #Radius of "spherical" earth
	#Coordinate offsets in radians
	dLat = dNorth/earth_radius
	dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

	#New position in decimal degrees
	newlat = original_location.lat + (dLat * 180/math.pi)
	newlon = original_location.lon + (dLon * 180/math.pi)
	if type(original_location) is LocationGlobal:
		targetlocation=LocationGlobal(newlat, newlon,altura)
	elif type(original_location) is LocationGlobalRelative:
		targetlocation=LocationGlobalRelative(newlat, newlon,altura) 
	return targetlocation