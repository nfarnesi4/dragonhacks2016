import serial
import time
import os, json
import ibmiotf.application
import uuid

def object_spec(values):
    return {
        'tanks' : [
            {
                'id' : i,
                'level': values[i]
            }
            for i in xrange(0, len(values))
        ]
    }
client = None

ser = serial.Serial("/dev/ttyUSB1")
ser.baudrate = 9600

try:
    options = ibmiotf.application.ParseConfigFile("/home/pi/device.cfg")
    client = ibmiotf.application.Client(options)
    client.connect()

    while ser.read(1) != "\n": pass
    while True:
        data = ser.read(1)
        recievedPacket = ""
        while data != "\n":
            recievedPacket += data
            data = ser.read(1)
        values = [int(svalue) for svalue in recievedPacket.split(", ")]
        myData = object_spec(values)
        print(myData)
        client.publishEvent("raspberrypi", options["id"], "status", "json" , myData)
        
        
except ibmiotf.ConnectionException  as e:
    print e

