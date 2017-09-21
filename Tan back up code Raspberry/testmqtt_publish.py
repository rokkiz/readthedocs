
from sense_hat import SenseHat
import paho.mqtt.publish as publish
import time
sense = SenseHat()

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
    sensor_data = [read_temp(), read_humidity(), read_pressure()]
    print("sending sensor data")
    publish.single("sensor", str(sensor_data), hostname="192.168.1.39")
    time.sleep(5)
    
