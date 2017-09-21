import sys
import time
from btle import *
from datetime import datetime
import calendar

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        #if isNewDev:
            #print ("Discovered device", dev.addr)
            #if dev.addr == "e2:01:00:01:c6:40":
               #print ("Received new data from %s, RSSI=%d dBm" % (dev.addr, dev.rssi)) 

        if isNewDev:
            if (dev.addr == "44:74:6c:9e:2b:b8") or (dev.addr == "b4:74:43:24:c9:30") or (dev.addr == "10:2A:B3:F5:D6:DC") or (dev.addr == "24:E3:14:90:9C:01") or (dev.addr == "58:48:22:9F:CA:04"):
                t = datetime.utcnow()
                timestamp=calendar.timegm(t.utctimetuple())
                print ("Date %s, Received new data from %s, RSSI=%d dBm" % (timestamp, dev.addr, dev.rssi))
##                print(dev.getScanData())
##                for (adtype, desc, value) in dev.getScanData():
##                    print ("  %s = %s" % (desc, value))
##                    print (" adtype %s" % adtype)

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(data)


######################## GET THE CHARACTERISTICS, SERVICES AND DESCRIPTORS ##################################
###per = Peripheral("c8:8c:29:e0:53:e6","random")
###f2:2b:64:71:03:05
###e2:01:00:01:f0:40
##per = Peripheral("c6:be:90:ba:c6:d5","random")
##per.setDelegate(MyDelegate())
##print("Connected")
##bleservices = per.getServices()
##for service in bleservices:
##    print(service.uuid)
##    print(service)
##print(bleservices)
##characteristics = per.getCharacteristics(startHnd=0x0001, endHnd=0xFFFF, uuid=None)
##for characteristic in characteristics:
##    print(characteristic.handle)
##    print("{}, hnd={}, supports {}".format(characteristic, hex(characteristic.handle), characteristic.propertiesToString()))
##    print(per.readCharacteristic(characteristic.handle))
##bledesc = per.getDescriptors()
##for desc in bledesc:
##    print(desc)
##per.disconnect()
##print("Disconnected")
###############################################################    
##try:
##    per.writeCharacteristic(14,bytes('aa','utf-8'))
##    print("writing done")
##    while True:
##        if per.waitForNotifications(1.0):
##            print("Notification")
##            continue
##    print("Waiting")
##finally:
##    per.disconnect()
##    print ("Disconnected")
                    
while True:
    scanner = Scanner().withDelegate(ScanDelegate()) #call class ScanDelegate()
    devices = scanner.scan()

