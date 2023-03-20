import os

def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20

#Reads Temperature Sensor in w1 devices
def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return farenheit

#Prints current temperature value in farenheit
def loop(ds18b20):
    #while True:
    if read(ds18b20) != None:
        print( "Current temperature : %0.3f F" % read(ds18b20))

def kill():
    quit()
