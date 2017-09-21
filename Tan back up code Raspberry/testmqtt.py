from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
sense = SenseHat()

Broker = "192.168.1.97"

sub_topic = "sensor/instructions"    # receive messages on this topic

pub_topic = "sensor/data"       # send messages to this topic


############### sensehat inputs ##################

def read_temp():
    t = sense.get_temperature()
    t = round(t)
    print("temperature",t)
    return t

def read_humidity():
    h = sense.get_humidity()
    h = round(h)
    print("humidity",h)
    return h

def read_pressure():
    p = sense.get_pressure()
    p = round(p)
    print("pressure",p)
    return p

def display_sensehat(message):
    sense.show_message(message)
    time.sleep(10)

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)
    display_sensehat(message)

def publish_mqtt(sensor_data):
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(Broker, 1883)
    mqttc.publish(pub_topic, sensor_data)
    #mqttc.loop(2) //timeout = 2s

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)


while True:
    sensor_data = [read_temp(), read_humidity(), read_pressure()]
    publish.single("monto/solar/sensors", str(sensor_data), hostname = Broker)
    time.sleep(1*60)
