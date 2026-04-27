# Import libraries
import time
import math
import datetime
import schedule
import paho.mqtt.publish as publish
import RPi.GPIO as io
io.setmode(io.BCM)

print("Hello, this is SqueakSpeed! Make sure you have plugged in the values correctly before running (Check psanosa GitHub to double-check input values!). This is tracking for Hall Sensors 1, 2, 3, 4, 5, and 6")

# Setup the pins of the Raspberry
# Pins for the wheel
hallsens_1 = INPUT VALUE HERE
hallsens_2 = INPUT VALUE HERE
hallsens_3 = INPUT VALUE HERE
hallsens_4 = INPUT VALUE HERE
hallsens_5 = INPUT VALUE HERE
hallsens_6 = INPUT VALUE HERE
# Setup wheel pins for Hall Sensors
io.setup(hallsens_1, io.IN, pull_up_down=io.PUD_UP)
io.setup(hallsens_2, io.IN, pull_up_down=io.PUD_UP)
io.setup(hallsens_3, io.IN, pull_up_down=io.PUD_UP)
io.setup(hallsens_4, io.IN, pull_up_down=io.PUD_UP)
io.setup(hallsens_5, io.IN, pull_up_down=io.PUD_UP)
io.setup(hallsens_6, io.IN, pull_up_down=io.PUD_UP)

# Circumference of mouse wheel 1
# Wheel diameter in m
wheeldiameter_1 = INPUT VALUE HERE
wheelsize_1 = wheeldiameter_1 * math.pi

# Circumference of mouse wheel 2
# Wheel diameter in m
wheeldiameter_2 = INPUT VALUE HERE
wheelsize_2 = wheeldiameter_2 * math.pi

# Circumference of mouse wheel 3
# Wheel diameter in m
wheeldiameter_3 = INPUT VALUE HERE
wheelsize_3 = wheeldiameter_3 * math.pi 

# Circumference of mouse wheel 4
# Wheel diameter in m
wheeldiameter_4 = INPUT VALUE HERE
wheelsize_4 = wheeldiameter_4 * math.pi

# Circumference of mouse wheel 5
# Wheel diameter in m
wheeldiameter_5 = INPUT VALUE HERE
wheelsize_5 = wheeldiameter_5 * math.pi 

# Circumference of mouse wheel 6
# Wheel diameter in m
wheeldiameter_6 = INPUT VALUE HERE
wheelsize_6 = wheeldiameter_6 * math.pi

# Number of wheel rotations for each hall sensor
rotations_1 = 0
rotations_2 = 0
rotations_3 = 0
rotations_4 = 0
rotations_5 = 0
rotations_6 = 0

# Distance covered in mouse wheel for each hall sensor  
sessionDistance_1 = 0
sessionDistance_2 = 0
sessionDistance_3 = 0
sessionDistance_4 = 0
sessionDistance_5 = 0
sessionDistance_6 = 0

# Speed for each hall sensor 
speed_1 = 0
speed_2 = 0 
speed_3 = 0
speed_4 = 0 
speed_5 = 0
speed_6 = 0 

# Acceleration for each hall sensor
acceleration_1 = 0 
acceleration_2 = 0
acceleration_3 = 0 
acceleration_4 = 0
acceleration_5 = 0 
acceleration_6 = 0

# Cumulative speed to get average for each hall sensor 
rotationSpeeds_1 = []
rotationSpeeds_2 = []
rotationSpeeds_3 = []
rotationSpeeds_4 = []
rotationSpeeds_5 = []
rotationSpeeds_6 = []

# Cumulative acceleration to get average for each hall sensor 
rotationAccelerations_1 = []
rotationAccelerations_2 = []
rotationAccelerations_3 = []
rotationAccelerations_4 = []
rotationAccelerations_5 = []
rotationAccelerations_6 = []

# Set the starttime to now
starttime_1 = datetime.datetime.now()
starttime_2 = datetime.datetime.now()
starttime_3 = datetime.datetime.now()
starttime_4 = datetime.datetime.now()
starttime_5 = datetime.datetime.now()
starttime_6 = datetime.datetime.now()


# Add a delay before performing calculations
time.sleep(3)  

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID for each Hall Sensor
channelID_1 = "INPUT VALUES HERE"
channelID_2 = "INPUT VALUES HERE"
channelID_3 = "INPUT VALUES HERE"
channelID_4 = "INPUT VALUES HERE"
channelID_5 = "INPUT VALUES HERE"
channelID_6 = "INPUT VALUES HERE"

# The Write API Key for the channel for each Hall Sensor 
apiKey_1 = "INPUT VALUES HERE"
apiKey_2 = "INPUT VALUES HERE"
apiKey_3 = "INPUT VALUES HERE"
apiKey_4 = "INPUT VALUES HERE"
apiKey_5 = "INPUT VALUES HERE"
apiKey_6 = "INPUT VALUES HERE"

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

# MQTT credentials for each Hall Sensor 
mqtt_client_ID_1 = "INPUT VALUES HERE"
mqtt_username_1 = "INPUT VALUES HERE"
mqtt_password_1 = "INPUT VALUES HERE"
mqtt_auth_1 = {'username':mqtt_username_1,'password':mqtt_password_1}

mqtt_client_ID_2 = "INPUT VALUES HERE"
mqtt_username_2 = "INPUT VALUES HERE"
mqtt_password_2 = "INPUT VALUES HERE"
mqtt_auth_2 = {'username':mqtt_username_2,'password':mqtt_password_2}

mqtt_client_ID_3 = "INPUT VALUES HERE"
mqtt_username_3 = "INPUT VALUES HERE"
mqtt_password_3 = "INPUT VALUES HERE"
mqtt_auth_3 = {'username':mqtt_username_3,'password':mqtt_password_3}

mqtt_client_ID_4 = "INPUT VALUES HERE"
mqtt_username_4 = "INPUT VALUES HERE"
mqtt_password_4 = "INPUT VALUES HERE"
mqtt_auth_4 = {'username':mqtt_username_4,'password':mqtt_password_4}

mqtt_client_ID_5 = "INPUT VALUES HERE"
mqtt_username_5 = "INPUT VALUES HERE"
mqtt_password_5 = "INPUT VALUES HERE"
mqtt_auth_5 = {'username':mqtt_username_5,'password':mqtt_password_5}

mqtt_client_ID_6 = "INPUT VALUES HERE"
mqtt_username_6  = "INPUT VALUES HERE"
mqtt_password_6  = "INPUT VALUES HERE"
mqtt_auth_6 = {'username':mqtt_username_6,'password':mqtt_password_6}

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

# Create the topic string for Hall Sensors
topic_1 = "channels/" + channelID_1 + "/publish" 
topic_2 = "channels/" + channelID_2 + "/publish" 
topic_3 = "channels/" + channelID_3 + "/publish" 
topic_4 = "channels/" + channelID_4 + "/publish" 
topic_5 = "channels/" + channelID_5 + "/publish" 
topic_6 = "channels/" + channelID_6 + "/publish" 

# Reset the wheel measurements for Hall Sensors
def resetValues_1():
    global sessionDistance_1
    global speed_1
    global rotations_1
    global acceleration_1
    print ('Before reset', sessionDistance_1, 'm (hall sensor 1)', speed_1, 'm/s (hall sensor 1)', rotations_1, 'rotations (hall sensor 1)', acceleration_1, 'm/s^2 (hall sensor 1)')
    sessionDistance_1 = 0
    speed_1 = 0
    rotations_1 = 0
    acceleration_1 = 0 
    print ('After reset', sessionDistance_1, 'm (hall sensor 1)', speed_1, 'm/s (hall sensor 1)', rotations_1, 'rotations (hall sensor 1)', acceleration_1, 'm/s^2 (hall sensor 1)')

def resetValues_2():
    global sessionDistance_2
    global speed_2
    global rotations_2
    global acceleration_2
    print ('Before reset', sessionDistance_2, 'm (hall sensor 2)', speed_2, 'm/s (hall sensor 2)', rotations_2, 'rotations (hall sensor 2)', acceleration_2, 'm/s^2 (hall sensor 2)')
    sessionDistance_2 = 0
    speed_2 = 0
    rotations_2 = 0
    acceleration_2 = 0 
    print ('After reset', sessionDistance_2, 'm (hall sensor 2)', speed_2, 'm/s (hall sensor 2)', rotations_2, 'rotations (hall sensor 2)', acceleration_2, 'm/s^2 (hall sensor 2)')

def resetValues_3():
    global sessionDistance_3
    global speed_3
    global rotations_3
    global acceleration_3
    print ('Before reset', sessionDistance_3, 'm (hall sensor 3)', speed_3, 'm/s (hall sensor 3)', rotations_3, 'rotations (hall sensor 3)', acceleration_3, 'm/s^2 (hall sensor 3)')
    sessionDistance_3 = 0
    speed_3 = 0
    rotations_3 = 0
    acceleration_3 = 0 
    print ('After reset', sessionDistance_3, 'm (hall sensor 3)', speed_3, 'm/s (hall sensor 3)', rotations_3, 'rotations (hall sensor 3)', acceleration_3, 'm/s^2 (hall sensor 3)')

def resetValues_4():
    global sessionDistance_4
    global speed_4
    global rotations_4
    global acceleration_4
    print ('Before reset', sessionDistance_4, 'm (hall sensor 4)', speed_4, 'm/s (hall sensor 4)', rotations_4, 'rotations (hall sensor 4)', acceleration_4, 'm/s^2 (hall sensor 4)')
    sessionDistance_4 = 0
    speed_4 = 0
    rotations_4 = 0
    acceleration_4 = 0 
    print ('After reset', sessionDistance_4, 'm (hall sensor 4)', speed_4, 'm/s (hall sensor 4)', rotations_4, 'rotations (hall sensor 4)', acceleration_4, 'm/s^2 (hall sensor 4)')

def resetValues_5():
    global sessionDistance_5
    global speed_5
    global rotations_5
    global acceleration_5
    print ('Before reset', sessionDistance_5, 'm (hall sensor 5)', speed_5, 'm/s (hall sensor 5)', rotations_5, 'rotations (hall sensor 5)', acceleration_5, 'm/s^2 (hall sensor 5)')
    sessionDistance_5 = 0
    speed_5 = 0
    rotations_5 = 0
    acceleration_5 = 0 
    print ('After reset', sessionDistance_5, 'm (hall sensor 5)', speed_5, 'm/s (hall sensor 5)', rotations_5, 'rotations (hall sensor 5)', acceleration_5, 'm/s^2 (hall sensor 5)')

def resetValues_6():
    global sessionDistance_6
    global speed_6
    global rotations_6
    global acceleration_6
    print ('Before reset', sessionDistance_6, 'm (hall sensor 6)', speed_6, 'm/s (hall sensor 6)', rotations_6, 'rotations (hall sensor 6)', acceleration_6, 'm/s^2 (hall sensor 6)')
    sessionDistance_6 = 0
    speed_6 = 0
    rotations_6 = 0
    acceleration_6 = 0 
    print ('After reset', sessionDistance_6, 'm (hall sensor 6)', speed_6, 'm/s (hall sensor 6)', rotations_6, 'rotations (hall sensor 6)', acceleration_6, 'm/s^2 (hall sensor 6)')


# Send IoT message to Thingspeak from hall sensor 
def sendMessage_1():
    print("Hello, this is SqueakSpeed from Hall Sensor 1.")
    print ('Minute Update from Hall Sensor 1', sessionDistance_1, 'm (hall sensor 1)', speed_1, 'm/s (hall sensor 1)', rotations_1, 'rotations (hall sensor 1)', acceleration_1, 'm/s^2 (hall sensor 1)')
    # Calculate average speed and acceleration per rotation
    if rotations_1 > 0:
        avgSpeed_1 = sum(rotationSpeeds_1) / rotations_1
        avgAcceleration_1 = sum(rotationAccelerations_1) / rotations_1
    else:
        avgSpeed_1 = 0
        avgAcceleration_1 = 0
    # Build the payload string
    tPayload_1 = "field1=" + str(rotations_1) + "&field2=" + str(sessionDistance_1) + "&field3=" + str(avgSpeed_1) + "&field4=" + str(avgAcceleration_1)
    # attempt to publish this data to the topic
    try:
        print ("Publishing Hall Sensor 1 data to thingspeak")
        print ("Writing Payload = ", tPayload_1," to host: ", mqtt_host)
        publish.single(topic_1, payload=tPayload_1, hostname=mqtt_host, port=tPort, tls=tTLS, transport=tTransport, client_id=mqtt_client_ID_1, auth=mqtt_auth_1)
        print ("ACTION COMPLETED: Published Hall Sensor 1 data to thingspeak.")
        # Clear the rotationSpeeds and rotationAccelerations lists
        rotationSpeeds_1.clear()
        rotationAccelerations_1.clear()
        resetValues_1() # Reset measurements
    
    except:
        print ("ACTION INCOMPLETE: Hall Sensor 1 data not published to Thingspeak due to connection error.")

    

def sendMessage_2():
    print("Hello, this is SqueakSpeed from Hall Sensor 2.")
    print ('Minute Update from Hall Sensor 2', sessionDistance_2, 'm (hall sensor 2)', speed_2, 'm/s (hall sensor 2)', rotations_2, 'rotations (hall sensor 2)', acceleration_2, 'm/s^2 (hall sensor 2)')
    # Calculate average speed and acceleration per rotation
    if rotations_2 > 0:
        avgSpeed_2 = sum(rotationSpeeds_2) / rotations_2
        avgAcceleration_2 = sum(rotationAccelerations_2) / rotations_2
    else:
        avgSpeed_2 = 0
        avgAcceleration_2 = 0
    # Build the payload string
    tPayload_2 = "field1=" + str(rotations_2) + "&field2=" + str(sessionDistance_2) + "&field3=" + str(avgSpeed_2) + "&field4=" + str(avgAcceleration_2)
    # attempt to publish this data to the topic
    try:
        print ("Publishing Hall Sensor 2 data to thingspeak")
        print ("Writing Payload = ", tPayload_2," to host: ", mqtt_host)
        publish.single(topic_2, payload=tPayload_2, hostname=mqtt_host, port=tPort, tls=tTLS, transport=tTransport, client_id=mqtt_client_ID_2, auth=mqtt_auth_2)
        print ("ACTION COMPLETED: Published Hall Sensor 2 data to thingspeak.")
        
        # Clear the rotationSpeeds and rotationAccelerations lists
        rotationSpeeds_2.clear()
        rotationAccelerations_2.clear()
        resetValues_2() # Reset measurements
        
    except:
        print ("ACTION INCOMPLETE: Hall Sensor 2 data not published to Thingspeak due to connection error.")
    

def sendMessage_3():
    
    print("Hello, this is SqueakSpeed from Hall Sensor 3.")
    print ('Minute Update from Hall Sensor 3', sessionDistance_3, 'm (hall sensor 3)', speed_3, 'm/s (hall sensor 3)', rotations_3, 'rotations (hall sensor 3)', acceleration_3, 'm/s^2 (hall sensor 3)')
    # Calculate average speed and acceleration per rotation
    if rotations_3 > 0:
        avgSpeed_3 = sum(rotationSpeeds_3) / rotations_3
        avgAcceleration_3 = sum(rotationAccelerations_3) / rotations_3
    else:
        avgSpeed_3 = 0
        avgAcceleration_3 = 0
    # Build the payload string
    tPayload_3 = "field1=" + str(rotations_3) + "&field2=" + str(sessionDistance_3) + "&field3=" + str(avgSpeed_3) + "&field4=" + str(avgAcceleration_3)
    # attempt to publish this data to the topic
    try:
        print ("Publishing Hall Sensor 3 data to thingspeak")
        print ("Writing Payload = ", tPayload_3," to host: ", mqtt_host)
        publish.single(topic_3, payload=tPayload_3, hostname=mqtt_host, port=tPort, tls=tTLS, transport=tTransport, client_id=mqtt_client_ID_3, auth=mqtt_auth_3)
        print ("ACTION COMPLETED: Published Hall Sensor 3 data to thingspeak.")
        
        # Clear the rotationSpeeds and rotationAccelerations lists
        rotationSpeeds_3.clear()
        rotationAccelerations_3.clear()
        resetValues_3() # Reset measurements

    except:
        print ("ACTION INCOMPLETE: Hall Sensor 3 data not published to Thingspeak due to connection error.")
    

def sendMessage_4():
    print("Hello, this is SqueakSpeed from Hall Sensor 4.")
    print ('Minute Update from Hall Sensor 4', sessionDistance_4, 'm (hall sensor 4)', speed_4, 'm/s (hall sensor 4)', rotations_4, 'rotations (hall sensor 4)', acceleration_4, 'm/s^2 (hall sensor 4)')
    
    # Calculate average speed and acceleration per rotation
    if rotations_4 > 0:
        avgSpeed_4 = sum(rotationSpeeds_4) / rotations_4
        avgAcceleration_4 = sum(rotationAccelerations_4) / rotations_4
    else:
        avgSpeed_4 = 0
        avgAcceleration_4 = 0
    # Build the payload string
    tPayload_4 = "field1=" + str(rotations_4) + "&field2=" + str(sessionDistance_4) + "&field3=" + str(avgSpeed_4) + "&field4=" + str(avgAcceleration_4)
    # attempt to publish this data to the topic
    try:
        print ("Publishing Hall Sensor 4 data to thingspeak")
        print ("Writing Payload = ", tPayload_4," to host: ", mqtt_host)
        publish.single(topic_4, payload=tPayload_4, hostname=mqtt_host, port=tPort, tls=tTLS, transport=tTransport, client_id=mqtt_client_ID_4, auth=mqtt_auth_4)
        print ("ACTION COMPLETED: Published Hall Sensor 4 data to thingspeak.")
        
        # Clear the rotationSpeeds and rotationAccelerations lists
        rotationSpeeds_4.clear()
        rotationAccelerations_4.clear()
        resetValues_4() # Reset measurements
    except:
        print ("ACTION INCOMPLETE: Hall Sensor 4 data not published to Thingspeak due to connection error.")


def sendMessage_5():
    print("Hello, this is SqueakSpeed from Hall Sensor 5.")
    print ('Minute Update from Hall Sensor 5', sessionDistance_5, 'm (hall sensor 5)', speed_5, 'm/s (hall sensor 5)', rotations_5, 'rotations (hall sensor 5)', acceleration_5, 'm/s^2 (hall sensor 5)')
    # Calculate average speed and acceleration per rotation
    if rotations_5 > 0:
        avgSpeed_5 = sum(rotationSpeeds_5) / rotations_5
        avgAcceleration_5 = sum(rotationAccelerations_5) / rotations_5
    else:
        avgSpeed_5 = 0
        avgAcceleration_5 = 0
    # Build the payload string
    tPayload_5 = "field1=" + str(rotations_5) + "&field2=" + str(sessionDistance_5) + "&field3=" + str(avgSpeed_5) + "&field4=" + str(avgAcceleration_5)
    # attempt to publish this data to the topic
    try:
        print ("Publishing Hall Sensor 5 data to thingspeak")
        print ("Writing Payload = ", tPayload_5," to host: ", mqtt_host)
        publish.single(topic_5, payload=tPayload_5, hostname=mqtt_host, port=tPort, tls=tTLS, transport=tTransport, client_id=mqtt_client_ID_5, auth=mqtt_auth_5)
        print ("ACTION COMPLETED: Published Hall Sensor 5 data to thingspeak.")
        
        # Clear the rotationSpeeds and rotationAccelerations lists
        rotationSpeeds_5.clear()
        rotationAccelerations_5.clear()
        resetValues_5() # Reset measurements

    except:
        print ("ACTION INCOMPLETE: Hall Sensor 5 data not published to Thingspeak due to connection error.")
    

def sendMessage_6():
    print("Hello, this is SqueakSpeed from Hall Sensor 6.")
    print ('Minute Update from Hall Sensor 6', sessionDistance_6, 'm (hall sensor 6)', speed_6, 'm/s (hall sensor 6)', rotations_6, 'rotations (hall sensor 6)', acceleration_6, 'm/s^2 (hall sensor 6)')
    
    # Calculate average speed and acceleration per rotation
    if rotations_6 > 0:
        avgSpeed_6 = sum(rotationSpeeds_6) / rotations_6
        avgAcceleration_6 = sum(rotationAccelerations_6) / rotations_6
    else:
        avgSpeed_6 = 0
        avgAcceleration_6 = 0
    # Build the payload string
    tPayload_6 = "field1=" + str(rotations_6) + "&field2=" + str(sessionDistance_6) + "&field3=" + str(avgSpeed_6) + "&field4=" + str(avgAcceleration_6)
    # attempt to publish this data to the topic
    try:
        print ("Publishing Hall Sensor 6 data to thingspeak")
        print ("Writing Payload = ", tPayload_6," to host: ", mqtt_host)
        publish.single(topic_6, payload=tPayload_6, hostname=mqtt_host, port=tPort, tls=tTLS, transport=tTransport, client_id=mqtt_client_ID_6, auth=mqtt_auth_6)
        print ("ACTION COMPLETED: Published Hall Sensor 6 data to thingspeak.")
        
        # Clear the rotationSpeeds and rotationAccelerations lists
        rotationSpeeds_6.clear()
        rotationAccelerations_6.clear()
        resetValues_6() # Reset measurements
    except:
        print ("ACTION INCOMPLETE: Hall Sensor 6 data not published to Thingspeak due to connection error.")


# Send a message every minute for Hall Sensors
schedule.every().minutes.do(sendMessage_1)
schedule.every().minutes.do(sendMessage_2)
schedule.every().minutes.do(sendMessage_3)
schedule.every().minutes.do(sendMessage_4)
schedule.every().minutes.do(sendMessage_5)
schedule.every().minutes.do(sendMessage_6)


# Function to calculate the current speed of the hamster wheel for Hall Sensors
def calculateSpeed_1(spintime_1):
    seconds_1 = spintime_1.total_seconds()
    currentSpeed_1 = wheelsize_1 / seconds_1
    return currentSpeed_1

def calculateSpeed_2(spintime_2):
    seconds_2 = spintime_2.total_seconds()
    currentSpeed_2 = wheelsize_2 / seconds_2
    return currentSpeed_2

def calculateSpeed_3(spintime_3):
    seconds_3 = spintime_3.total_seconds()
    currentSpeed_3 = wheelsize_3 / seconds_3
    return currentSpeed_3

def calculateSpeed_4(spintime_4):
    seconds_4 = spintime_4.total_seconds()
    currentSpeed_4 = wheelsize_4 / seconds_4
    return currentSpeed_4

def calculateSpeed_5(spintime_5):
    seconds_5 = spintime_5.total_seconds()
    currentSpeed_5 = wheelsize_5 / seconds_5
    return currentSpeed_5

def calculateSpeed_6(spintime_6):
    seconds_6 = spintime_6.total_seconds()
    currentSpeed_6 = wheelsize_6 / seconds_6
    return currentSpeed_6

# Function to calculate the current acceleration of the hamster wheel for Hall Sensors
def calculateAcceleration_1(spintime_1, previousSpeed_1):
    seconds_1 = spintime_1.total_seconds()
    currentSpeed_1 = wheelsize_1 / seconds_1
    currentAcceleration_1 = (currentSpeed_1 - previousSpeed_1) / seconds_1
    return currentAcceleration_1

def calculateAcceleration_2(spintime_2, previousSpeed_2):
    seconds_2 = spintime_2.total_seconds()
    currentSpeed_2 = wheelsize_2 / seconds_2 
    currentAcceleration_2 = (currentSpeed_2 - previousSpeed_2) / seconds_2
    return currentAcceleration_2

def calculateAcceleration_3(spintime_3, previousSpeed_3):
    seconds_3 = spintime_3.total_seconds()
    currentSpeed_3 = wheelsize_3 / seconds_3
    currentAcceleration_3 = (currentSpeed_3 - previousSpeed_3) / seconds_3
    return currentAcceleration_3

def calculateAcceleration_4(spintime_4, previousSpeed_4):
    seconds_4 = spintime_4.total_seconds()
    currentSpeed_4 = wheelsize_4 / seconds_4
    currentAcceleration_4 = (currentSpeed_4 - previousSpeed_4) / seconds_4
    return currentAcceleration_4

def calculateAcceleration_5(spintime_5, previousSpeed_5):
    seconds_5 = spintime_5.total_seconds()
    currentSpeed_5 = wheelsize_5 / seconds_5
    currentAcceleration_5 = (currentSpeed_5 - previousSpeed_5) / seconds_5
    return currentAcceleration_5

def calculateAcceleration_6(spintime_6, previousSpeed_6):
    seconds_6 = spintime_6.total_seconds()
    currentSpeed_6 = wheelsize_6 / seconds_6
    currentAcceleration_6 = (currentSpeed_6 - previousSpeed_6) / seconds_6
    return currentAcceleration_6

# Variables to store previous speed for Hall Sensors
previousSpeed_1 = 0
previousSpeed_2 = 0
previousSpeed_3 = 0
previousSpeed_4 = 0
previousSpeed_5 = 0
previousSpeed_6 = 0

# Variables to store previous acceleration for Hall Sensors
previousAcceleration_1 = 0 
previousAcceleration_2 = 0 
previousAcceleration_3 = 0 
previousAcceleration_4 = 0 
previousAcceleration_5 = 0 
previousAcceleration_6 = 0 

# Define the maximum duration of the stationary period in seconds for Hall Sensors
max_stationary_duration_1 = 3
max_stationary_duration_2 = 3
max_stationary_duration_3 = 3
max_stationary_duration_4 = 3
max_stationary_duration_5 = 3
max_stationary_duration_6 = 3

# Variables to track the state and time for Hall Sensors
rotation_detected_1 = False
detection_start_time_1 = None
previous_state_1 = 0 # Initialize previous state to 0 

rotation_detected_2 = False
detection_start_time_2 = None
previous_state_2 = 0 # Initialize previous state to 0 

rotation_detected_3 = False
detection_start_time_3 = None
previous_state_3 = 0 # Initialize previous state to 0 

rotation_detected_4 = False
detection_start_time_4 = None
previous_state_4 = 0 # Initialize previous state to 0 

rotation_detected_5 = False
detection_start_time_5 = None
previous_state_5 = 0 # Initialize previous state to 0 

rotation_detected_6 = False
detection_start_time_6 = None
previous_state_6 = 0 # Initialize previous state to 0 

# While the script runs
while True:
    # Check the pending scheduled tasks
    schedule.run_pending()

    # Read the current state for each of the hall sensors
    current_state_1 = io.input(hallsens_1)
    current_state_2 = io.input(hallsens_2)
    current_state_3 = io.input(hallsens_3)
    current_state_4 = io.input(hallsens_4)
    current_state_5 = io.input(hallsens_5)
    current_state_6 = io.input(hallsens_6)

    # When the magnet passes the hall sensor, one rotation has happened for Hall Sensor 1
    if current_state_1 == 0 and previous_state_1 == 1:
        # Check if the previous state was stationary
        if rotation_detected_1:
            # Calculate the duration of the stationary period
            detection_start_time_1 = (datetime.datetime.now() - detection_start_time_1).total_seconds()

            # Check if the stationary duration is within the desired range
            if detection_start_time_1 >= 0 and detection_start_time_1 < max_stationary_duration_1:
                # The end of the rotation is now
                endtime_1 = datetime.datetime.now()
                # The time spent spinning was the endtime - starttime
                spintime_1 = endtime_1 - starttime_1
                # New starttime is the endtime
                starttime_1 = endtime_1
                # Calculating the speed based on the spintime
                speed_1 = calculateSpeed_1(spintime_1)
                # Calculating the acceleration based on spintime and previous speed
                acceleration_1 = calculateAcceleration_1(spintime_1, previousSpeed_1)
                # Update the previous speed and acceleration for the next iteration
                previousSpeed_1 = speed_1
                previousAcceleration_1 = acceleration_1
                # Calculating the distance covered
                sessionDistance_1 = sessionDistance_1 + wheelsize_1
                # Calculating the amount of rotations
                rotations_1 += 1
                # Append calculated speeds and acceleration to the list
                rotationSpeeds_1.append(speed_1)
                rotationAccelerations_1.append(acceleration_1)
                    
                # Print to console and sleep
                print (sessionDistance_1, 'm (hall sensor 1)', speed_1, 'm/s (hall sensor 1)', rotations_1, 'rotations (hall sensor 1)', acceleration_1, 'm/s^2 (hall sensor 1)')
                time.sleep(0.05)
        
        # Reset rotation detection if duration exceeds the maximum
        rotation_detected_1 = False
        detection_start_time_1 = None

    # Check if the current state is stationary
    if current_state_1 == 1:
        # Set the stationary flag and start time if not already set
        if not rotation_detected_1:
            rotation_detected_1 = True
            detection_start_time_1 = datetime.datetime.now()
    
    # Update previous state
    previous_state_1 = current_state_1



    # When the magnet passes the hall sensor, one rotation has happened for Hall Sensor 2
    if current_state_2 == 0 and previous_state_2 == 1:
        # Check if the previous state was stationary
        if rotation_detected_2:
            # Calculate the duration of the stationary period
            detection_start_time_2 = (datetime.datetime.now() - detection_start_time_2).total_seconds()

            # Check if the stationary duration is within the desired range
            if detection_start_time_2 >= 0 and detection_start_time_2 < max_stationary_duration_2:
                # The end of the rotation is now
                endtime_2 = datetime.datetime.now()
                # The time spent spinning was the endtime - starttime
                spintime_2 = endtime_2 - starttime_2
                # New starttime is the endtime
                starttime_2 = endtime_2
                # Calculating the speed based on the spintime
                speed_2 = calculateSpeed_2(spintime_2)
                # Calculating the acceleration based on spintime and previous speed
                acceleration_2 = calculateAcceleration_2(spintime_2, previousSpeed_2)
                # Update the previous speed and acceleration for the next iteration
                previousSpeed_2 = speed_2
                previousAcceleration_2 = acceleration_2
                # Calculating the distance covered
                sessionDistance_2 = sessionDistance_2 + wheelsize_2
                # Calculating the amount of rotations
                rotations_2 += 1
                # Append calculated speeds and acceleration to the list
                rotationSpeeds_2.append(speed_2)
                rotationAccelerations_2.append(acceleration_2)
                    
                # Print to console and sleep
                print (sessionDistance_2, 'm (hall sensor 2)', speed_2, 'm/s (hall sensor 2)', rotations_2, 'rotations (hall sensor 2)', acceleration_2, 'm/s^2 (hall sensor 2)')
                time.sleep(0.05)
        
        # Reset rotation detection if duration exceeds the maximum
        rotation_detected_2 = False
        detection_start_time_2 = None

    # Check if the current state is stationary
    if current_state_2 == 1:
        # Set the stationary flag and start time if not already set
        if not rotation_detected_2:
            rotation_detected_2 = True
            detection_start_time_2 = datetime.datetime.now()
    
    # Update previous state
    previous_state_2 = current_state_2

    

    # When the magnet passes the hall sensor, one rotation has happened for Hall Sensor 3
    if current_state_3 == 0 and previous_state_3 == 1:
        # Check if the previous state was stationary
        if rotation_detected_3:
            # Calculate the duration of the stationary period
            detection_start_time_3 = (datetime.datetime.now() - detection_start_time_3).total_seconds()

            # Check if the stationary duration is within the desired range
            if detection_start_time_3 >= 0 and detection_start_time_3 < max_stationary_duration_3:
                # The end of the rotation is now
                endtime_3 = datetime.datetime.now()
                # The time spent spinning was the endtime - starttime
                spintime_3 = endtime_3 - starttime_3
                # New starttime is the endtime
                starttime_3 = endtime_3
                # Calculating the speed based on the spintime
                speed_3 = calculateSpeed_3(spintime_3)
                # Calculating the acceleration based on spintime and previous speed
                acceleration_3 = calculateAcceleration_3(spintime_3, previousSpeed_3)
                # Update the previous speed and acceleration for the next iteration
                previousSpeed_3 = speed_3
                previousAcceleration_3 = acceleration_3
                # Calculating the distance covered
                sessionDistance_3 = sessionDistance_3 + wheelsize_3
                # Calculating the amount of rotations
                rotations_3 += 1
                # Append calculated speeds and acceleration to the list
                rotationSpeeds_3.append(speed_3)
                rotationAccelerations_3.append(acceleration_3)
                    
                # Print to console and sleep
                print (sessionDistance_3, 'm (hall sensor 3)', speed_3, 'm/s (hall sensor 3)', rotations_3, 'rotations (hall sensor 3)', acceleration_3, 'm/s^2 (hall sensor 3)')
                time.sleep(0.05)
        
        # Reset rotation detection if duration exceeds the maximum
        rotation_detected_3 = False
        detection_start_time_3 = None

    # Check if the current state is stationary
    if current_state_3 == 1:
        # Set the stationary flag and start time if not already set
        if not rotation_detected_3:
            rotation_detected_3 = True
            detection_start_time_3 = datetime.datetime.now()
    
    # Update previous state
    previous_state_3 = current_state_3



    # When the magnet passes the hall sensor, one rotation has happened for Hall Sensor 4
    if current_state_4 == 0 and previous_state_4 == 1:
        # Check if the previous state was stationary
        if rotation_detected_4:
            # Calculate the duration of the stationary period
            detection_start_time_4 = (datetime.datetime.now() - detection_start_time_4).total_seconds()

            # Check if the stationary duration is within the desired range
            if detection_start_time_4 >= 0 and detection_start_time_4 < max_stationary_duration_4:
                # The end of the rotation is now
                endtime_4 = datetime.datetime.now()
                # The time spent spinning was the endtime - starttime
                spintime_4 = endtime_4 - starttime_4
                # New starttime is the endtime
                starttime_4 = endtime_4
                # Calculating the speed based on the spintime
                speed_4 = calculateSpeed_4(spintime_4)
                # Calculating the acceleration based on spintime and previous speed
                acceleration_4 = calculateAcceleration_4(spintime_4, previousSpeed_4)
                # Update the previous speed and acceleration for the next iteration
                previousSpeed_4 = speed_4
                previousAcceleration_4 = acceleration_4
                # Calculating the distance covered
                sessionDistance_4 = sessionDistance_4 + wheelsize_4
                # Calculating the amount of rotations
                rotations_4 += 1
                # Append calculated speeds and acceleration to the list
                rotationSpeeds_4.append(speed_4)
                rotationAccelerations_4.append(acceleration_4)
                    
                # Print to console and sleep
                print (sessionDistance_4, 'm (hall sensor 4)', speed_4, 'm/s (hall sensor 4)', rotations_4, 'rotations (hall sensor 4)', acceleration_4, 'm/s^2 (hall sensor 4)')
                time.sleep(0.05)
        
        # Reset rotation detection if duration exceeds the maximum
        rotation_detected_4 = False
        detection_start_time_4 = None

    # Check if the current state is stationary
    if current_state_4 == 1:
        # Set the stationary flag and start time if not already set
        if not rotation_detected_4:
            rotation_detected_4 = True
            detection_start_time_4 = datetime.datetime.now()
    
    # Update previous state
    previous_state_4 = current_state_4



    # When the magnet passes the hall sensor, one rotation has happened for Hall Sensor 5
    if current_state_5 == 0 and previous_state_5 == 1:
        # Check if the previous state was stationary
        if rotation_detected_5:
            # Calculate the duration of the stationary period
            detection_start_time_5 = (datetime.datetime.now() - detection_start_time_5).total_seconds()

            # Check if the stationary duration is within the desired range
            if detection_start_time_5 >= 0 and detection_start_time_5 < max_stationary_duration_5:
                # The end of the rotation is now
                endtime_5 = datetime.datetime.now()
                # The time spent spinning was the endtime - starttime
                spintime_5 = endtime_5 - starttime_5
                # New starttime is the endtime
                starttime_5 = endtime_5
                # Calculating the speed based on the spintime
                speed_5 = calculateSpeed_5(spintime_5)
                # Calculating the acceleration based on spintime and previous speed
                acceleration_5 = calculateAcceleration_5(spintime_5, previousSpeed_5)
                # Update the previous speed and acceleration for the next iteration
                previousSpeed_5 = speed_5
                previousAcceleration_5 = acceleration_5
                # Calculating the distance covered
                sessionDistance_5 = sessionDistance_5 + wheelsize_5
                # Calculating the amount of rotations
                rotations_5 += 1
                # Append calculated speeds and acceleration to the list
                rotationSpeeds_5.append(speed_5)
                rotationAccelerations_5.append(acceleration_5)
                    
                # Print to console and sleep
                print (sessionDistance_5, 'm (hall sensor 5)', speed_5, 'm/s (hall sensor 5)', rotations_5, 'rotations (hall sensor 5)', acceleration_5, 'm/s^2 (hall sensor 5)')
                time.sleep(0.05)
        
        # Reset rotation detection if duration exceeds the maximum
        rotation_detected_5 = False
        detection_start_time_5 = None

    # Check if the current state is stationary
    if current_state_5 == 1:
        # Set the stationary flag and start time if not already set
        if not rotation_detected_5:
            rotation_detected_5 = True
            detection_start_time_5 = datetime.datetime.now()
    
    # Update previous state
    previous_state_5 = current_state_5



    # When the magnet passes the hall sensor, one rotation has happened for Hall Sensor 6
    if current_state_6 == 0 and previous_state_6 == 1:
        # Check if the previous state was stationary
        if rotation_detected_6:
            # Calculate the duration of the stationary period
            detection_start_time_6 = (datetime.datetime.now() - detection_start_time_6).total_seconds()

            # Check if the stationary duration is within the desired range
            if detection_start_time_6 >= 0 and detection_start_time_6 < max_stationary_duration_6:
                # The end of the rotation is now
                endtime_6 = datetime.datetime.now()
                # The time spent spinning was the endtime - starttime
                spintime_6 = endtime_6 - starttime_6
                # New starttime is the endtime
                starttime_6 = endtime_6
                # Calculating the speed based on the spintime
                speed_6 = calculateSpeed_6(spintime_6)
                # Calculating the acceleration based on spintime and previous speed
                acceleration_6 = calculateAcceleration_6(spintime_6, previousSpeed_6)
                # Update the previous speed and acceleration for the next iteration
                previousSpeed_6 = speed_6
                previousAcceleration_6 = acceleration_6
                # Calculating the distance covered
                sessionDistance_6 = sessionDistance_6 + wheelsize_6
                # Calculating the amount of rotations
                rotations_6 += 1
                # Append calculated speeds and acceleration to the list
                rotationSpeeds_6.append(speed_6)
                rotationAccelerations_6.append(acceleration_6)
                    
                # Print to console and sleep
                print (sessionDistance_6, 'm (hall sensor 6)', speed_6, 'm/s (hall sensor 6)', rotations_6, 'rotations (hall sensor 6)', acceleration_6, 'm/s^2 (hall sensor 6)')
                time.sleep(0.05)
        
        # Reset rotation detection if duration exceeds the maximum
        rotation_detected_6 = False
        detection_start_time_6 = None

    # Check if the current state is stationary
    if current_state_6 == 1:
        # Set the stationary flag and start time if not already set
        if not rotation_detected_6:
            rotation_detected_6 = True
            detection_start_time_6 = datetime.datetime.now()
    
    # Update previous state
    previous_state_6 = current_state_6