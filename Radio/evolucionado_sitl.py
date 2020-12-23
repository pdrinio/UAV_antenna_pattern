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

# Tells APM to RTL without changing height
dron.parameters['RTL_ALT'] = 0

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

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
    dron.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print (" Altitude: ", dron.location.global_relative_frame.alt )
        #Break and return from function just below target altitude.        
        if dron.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print ("Reached target altitude")
            break
        time.sleep(1)
		
arm_and_takeoff(2)

print ("Set default/target airspeed to 2")
dron.airspeed = 2

print ("Going towards first point for 20 seconds ...")
point1 = LocationGlobalRelative(42.3961659, -8.7088215, 2)
dron.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(20)

print ("Going towards second point for 20 seconds (groundspeed set to 3 m/s) ...")
point2 = LocationGlobalRelative(42.3959688, -8.7086579, 2)
dron.simple_goto(point2, groundspeed=3)

# sleep so we can see the change in map
time.sleep(20)

print ("Returning to Launch")
dron.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print ("Close vehicle object")
dron.close()