import subprocess

#def launchSitl():
#    openCMD='START CMD /K '
#    sitlRoute='"C:\\Users\\jnunez\\Documents\\Mission Planner\\sitl\\ArduCopter.exe" '
#    sitlArgs='--model hexa --home=42.396695,-8.708492,0,0'
#    subprocess.call(openCMD + sitlRoute + sitlArgs, shell=True)
#
#launchSitl()



connection_string = "tcp:127.0.0.1:5762"

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
dron = connect(connection_string, wait_ready=False)
		
print ("Basic pre-arm checks")
# Don't try to arm until autopilot is ready
while not dron.is_armable:
    print (" Waiting for vehicle to initialise...")
    time.sleep(1)

    
print ("Arming motors")
# Copter should arm in GUIDED mode
dron.mode = VehicleMode("GUIDED")
dron.armed = True    

# Confirm vehicle armed before attempting to take off
while not dron.armed:      
    print (" Waiting for arming...")
    time.sleep(1)

print ("Taking off!")

#print ("Set default/target airspeed to 1")
dron.groundspeed = 0.25

print ("Going towards first point for 10 seconds ...")
point1 = LocationGlobalRelative(42.3961659, -8.7088215, 0)
dron.simple_goto(point1,groundspeed=0.25)

# sleep so we can see the change in map
time.sleep(10)

print ("Going towards second point for 10 seconds (groundspeed set to 1 m/s) ...")
point2 = LocationGlobalRelative(42.3959688, -8.7086579, 0)
dron.simple_goto(point2, groundspeed=0.25)

# sleep so we can see the change in map
time.sleep(10)

print ("Returning to Launch")
dron.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print ("Close vehicle object")
dron.close()