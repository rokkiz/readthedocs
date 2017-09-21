'''
Inspectorio Real-time Location Tracking and Environment Monitoring
May, 2017
 '''
from sense_hat import SenseHat
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from btle import Scanner, DefaultDelegate
import sys
import logging
import time
import getopt
import json
import calendar
from datetime import datetime
sense = SenseHat()


#Read MACaddress
mac = str(open('/sys/class/net/eth0/address').read())
#print(mac)#b8:27:eb:c9:17:19
# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------")

# Usage
usageInfo = """Usage:

Use certificate based mutual authentication:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

Use MQTT over WebSocket:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

Type "python basicPubSub.py -h" for available options.
"""
# Help info
helpInfo = """-e, --endpoint
	Your AWS IoT custom endpoint
-r, --rootCA
	Root CA file path
-c, --cert
	Certificate file path
-k, --key
	Private key file path
-w, --websocket
	Use MQTT over WebSocket
-h, --help
	Help information


"""

# Read in command-line parameters
# Point exactly the file path
# Download the connect-device-package.zip on AWS IoT and unzip it to get the new certificate and key
useWebsocket = False
host = "a38thfmd0ww5o2.iot.ap-southeast-1.amazonaws.com"
rootCAPath = "/home/pi/Downloads/root-CA.crt"
certificatePath = "/home/pi/Downloads/Raspberry_Pi3.cert.pem"
privateKeyPath = "/home/pi/Downloads/Raspberry_Pi3.private.key"

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)




streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
mycount = 1
myAWSIoTMQTTClient = None

if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)#auto-reconnect backoff to start with 1 second and use 32 seconds as maximum back off time. Connection over 20 second is considered stable.
        #configure the offline queue for publish requests to be 20 in size and drop the oldest request when the queue is full
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing (0 is disable)
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        #used to configure the time in seconds to wait for a connect or a disconnect to complete
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT

#myAWSIoTMQTTClient.connect()

#while True:
        #myAWSIoTMQTTClient.subscribe("sdk/test/Python", 1, customCallback)
        #time.sleep(2)

############### sensehat inputs ##################

def read_temp():
    t = sense.get_temperature()
    t = round(t)
    #print("temperature",t)
    return t

def read_humidity():
    h = sense.get_humidity()
    h = round(h)
    #print("humidity",h)
    return h

def read_pressure():
    p = sense.get_pressure()
    p = round(p)
    #print("pressure",p)
    return p
def display_sensehat(message):
    sense.show_message(message)
    time.sleep(10)


############### BLE data transfer ##################
class ScanDelegate(DefaultDelegate):
    #global mycount
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        global mycount
        if isNewData:
            logfile = open("/home/pi/logmqtt.txt","a")
            if dev.addr == "e2:01:00:02:44:40":
                #t = str(datetime.utcnow())
                t = str(int(round(time.time()*1000)))
                #timestamp=calendar.timegm(t.utctimetuple())
                BLEdata = {
                        "no": mycount,
                        "timestamp": t,
                        "device_id": dev.addr,
                        "rssi": dev.rssi,
                         "gateway_id": mac.strip()}
                print("Sending BLE data")
                myAWSIoTMQTTClient.publish(mac.strip() + "/ble", json.dumps(BLEdata), 1)
                logfile.write("%s\n" % str(BLEdata))
                mycount +=1
                    
###############################################################################
    
# Publish to the same topic in a loop forever

while True:
    scanner = Scanner().withDelegate(ScanDelegate()) #call class ScanDelegate()
    devices = scanner.scan(10)
    t = str(int(round(time.time()*1000)))
    sensor_data = {
            "timestamp": t,
            "temp": read_temp(),
            "humidity": read_humidity(),
            "pressure":read_pressure(),
             "gateway_id": mac.strip()}   
    print("sending sensor data")
    myAWSIoTMQTTClient.publish(mac.strip() + "/sensor", json.dumps(sensor_data), 1)
    time.sleep(0)
