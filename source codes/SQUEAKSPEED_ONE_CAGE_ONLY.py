# Import libraries
import time
import math
import datetime
import schedule
import paho.mqtt.publish as publish
import RPi.GPIO as io
io.setmode(io.BCM)

print("Hello, this is SqueakSpeed! Make sure you have plugged in the values correctly before running (Check psanosa GitHub to double-check input values!)")

#Setup the pins of the Raspberry
# Pin for the wheel
wheelpin = INPUT VALUE HERE
# Setup wheel pin
io.setup(wheelpin, io.IN, pull_up_down=io.PUD_UP)

# Circumference of mouse wheel
# Wheel diameter in m
wheeldiameter = INPUT VALUE HERE
wheelsize = math.pi * wheeldiameter

# Number of wheel rotations
rotations = 0

# Distance covered in mouse wheel per run session
sessionDistance = 0

# Speed
speed = 0

# Acceleration
acceleration = 0 

# Cumulative speeds to get average
rotationSpeeds = []

# Cumulative acceleration to get average
rotationAccelerations = []

# Set the starttime to now
starttime = datetime.datetime.now()

# Add a delay before performing calculations
time.sleep(5) 


#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
channelID = "INPUT VALUES HERE"

# The Write API Key for the channel
apiKey = "INPUT VALUES HERE"

#  MQTT Connection Methods
# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = False

# Set useUnsecuredWebSockets True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False 

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = True   

# The Hostname of the ThingSpeak MQTT service
mqtt_host = "mqtt3.thingspeak.com"

# MQTT credentials for the device
mqtt_client_ID = "INPUT VALUES HERE"
mqtt_username  = "INPUT VALUES HERE"
mqtt_password  = "INPUT VALUES HERE"
mqtt_auth = {'username':mqtt_username,'password':mqtt_password}

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443

# Create the topic string
topic = "channels/" + channelID + "/publish" 

# Reset the wheel measurements
def resetValues():
    global sessionDistance
    global speed
    global rotations
    global acceleration
    print ('Before reset', sessionDistance, 'm', speed, 'm/s', rotations, 'rotations', acceleration, 'm/s^2')
    sessionDistance = 0
    speed = 0
    rotations = 0
    acceleration = 0 
    print ('After reset', sessionDistance, 'm', speed, 'm/s', rotations, 'rotations', acceleration, 'm/s^2')
    

# Send IoT message to Thingspeak
def sendMessage():
    print("Hello, this is SqueakSpeed.")
    print ('Minute Update', sessionDistance, 'm', speed, 'm/s', rotations, 'rotations', acceleration, 'm/s^2')
    # Calculate average speed and acceleration per rotation
    if rotations > 0:
        avgSpeed = sum(rotationSpeeds) / rotations
        avgAcceleration = sum(rotationAccelerations) / rotations
    else:
        avgSpeed = 0
        avgAcceleration = 0

    # Build the payload string
    tPayload = "field1=" + str(rotations) + "&field2=" + str(sessionDistance) + "&field3=" + str(avgSpeed) + "&field4=" + str(avgAcceleration)
    # attempt to publish this data to the topic
    try:
        print ("Publishing data to thingspeak")
        print ("Writing Payload = ", tPayload," to host: ", mqtt_host)
        publish.single(topic, payload=tPayload, hostname=mqtt_host, port=tPort, tls=tTLS, transport=tTransport, client_id=mqtt_client_ID, auth=mqtt_auth)
        print ("ACTION COMPLETED: Published data to thingspeak.")

        # Clear the rotationSpeeds and rotationAccelerations lists
        rotationSpeeds.clear()
        rotationAccelerations.clear()
        resetValues() # Reset measurements

    except:
        print ("ACTION INCOMPLETE: Data not published to Thingspeak due to connection error.")
        

# Send a message every minute
schedule.every().minutes.do(sendMessage)


# Function to calculate the current speed of the hamster wheel
def calculateSpeed(spintime):
    seconds = spintime.total_seconds()
    currentSpeed = wheelsize / seconds
    return currentSpeed

# Function to calculate the current acceleration of the hamster wheel
def calculateAcceleration(spintime, previousSpeed):
    seconds = spintime.total_seconds()
    currentSpeed = wheelsize / seconds 
    currentAcceleration = (currentSpeed - previousSpeed) / seconds 
    return currentAcceleration

# Variables to store previous speed and acceleration
previousSpeed = 0
previousAcceleration = 0 

# Define the maximum duration of the stationary period in seconds
max_stationary_duration = 3

# Variables to track the state and time
rotation_detected = False
detection_start_time = None
previous_state = 0 # Initialize previous state to 0 

# While the script runs
while True:
    # Check the pending scheduled tasks
    schedule.run_pending()

    # Read the current state of the hall sensor
    current_state = io.input(wheelpin)

    # When the magnet passes the hall sensor, one rotation has happened
    if io.input(wheelpin) == 0 and previous_state == 1:
        # Check if the previous state was stationary
        if rotation_detected:
            # Calculate the duration of the stationary period
            detection_start_time = (datetime.datetime.now() - detection_start_time).total_seconds()

            # Check if the stationary duration is within the desired range
            if detection_start_time >= 0 and detection_start_time < max_stationary_duration:
                # The end of the rotation is now
                endtime = datetime.datetime.now()
                # The time spent spinning was the endtime - starttime
                spintime = endtime - starttime
                # New starttime is the endtime
                starttime = endtime
                # Calculating the speed based on the spintime
                speed = calculateSpeed(spintime)
                # Calculating the acceleration based on spintime and previous speed
                acceleration = calculateAcceleration(spintime, previousSpeed)
                # Update the previous speed and acceleration for the next iteration
                previousSpeed = speed
                previousAcceleration = acceleration 
                # Calculating the distance covered
                sessionDistance = sessionDistance + wheelsize
                # Calculating the amount of rotations
                rotations += 1
                # Append calculated speeds and acceleration to the list
                rotationSpeeds.append(speed)
                rotationAccelerations.append(acceleration)
                    
                # Print to console and sleep
                print (sessionDistance, 'm', speed, 'm/s', rotations, 'rotations', acceleration, 'm/s^2')
                time.sleep(0.05)
    
        # Reset rotation detection if magnet is not detected
        rotation_detected = False
        detection_start_time = None

    # Check if the current state is stationary
    if current_state == 1:
        # Set the stationary flag and start time if not already set
        if not rotation_detected:
            rotation_detected = True
            detection_start_time = datetime.datetime.now()

    # Update previous state
    previous_state = current_state