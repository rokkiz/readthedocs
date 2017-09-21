from sense_hat import SenseHat
import sys
from datetime import datetime
import paho.mqtt.publish as publish
import time
import json

sense = SenseHat()
mac = str(open('/sys/class/net/eth0/address').read())
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
    
while True:
    t=str(datetime.now())
    sensor_data = {
            "timestamp": t,
            "temp": read_temp(),
            "humidity": read_humidity(),
            "pressure":read_pressure(),
             "gateway_id": mac.strip()}
    print("Sending sensor data")
    publish.single("sensor",json.dumps(sensor_data),hostname = "192.168.1.20")
    #sense.set_pixel(0,2,(0,0,255))
    time.sleep(5)










