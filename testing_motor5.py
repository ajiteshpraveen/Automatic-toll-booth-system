import serial #Serial imported for Serial communication
import time #Required to use delay functions
 
ArduinoSerial = serial.Serial('/dev/ttyACM0',9600) #Create Serial port object called arduinoSerialData
time.sleep(2) #wait for 2 secounds for the communication to get established
 #read the serial data and print it as line
print ("Gate is opening")

ArduinoSerial.write(1) #send 1
print ("turned ON")
time.sleep(6)

