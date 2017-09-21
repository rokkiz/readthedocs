import sys
import time
#import paho.mqtt.publish as publish
from btle import Scanner, DefaultDelegate
from datetime import datetime
import json
mycount = 1
mac = str(open('/sys/class/net/eth0/address').read())
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        #if isNewDev:
            #print ("Discovered device", dev.addr)
            #if dev.addr == "e2:01:00:01:c6:40":
               #print ("Received new data from %s, RSSI=%d dBm" % (dev.addr, dev.rssi))
        #(dev.addr == "e2:01:00:02:0d:40") or 
        #(dev.addr == "e2:01:00:02:44:40") or (dev.addr == "e2:01:00:01:b6:40") or (dev.addr =="e2:01:00:01:f0:40")
        if dev.addr == "e2:01:00:01:f0:40":
            global mycount
            logfile = open("/home/pi/logmqtt.txt","a")
            t = str(datetime.utcnow())
            #if isNewData:  
            BLEdata = {
                        "no": mycount,
                        "timestamp": t,
                        "device_id": dev.addr,
                        "rssi": dev.rssi,
                         "gateway_id": mac.strip()}
            print ("Received new data from", json.dumps(BLEdata))
            logfile.write("%s\n" % str(BLEdata))
            mycount +=1
                #publish.single("BLE", dev.addr + dev.rssi, hostname="192.168.1.61")
                #for (adtype, desc, value) in dev.getScanData():
                    #print ("  %s = %s" % (desc, value))
while True:
    scanner = Scanner().withDelegate(ScanDelegate()) #call class ScanDelegate()
    devices = scanner.scan()
    time.sleep(1)



