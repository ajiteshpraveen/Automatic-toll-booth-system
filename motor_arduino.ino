//ERFINDER CODE
#include <SoftwareSerial.h>
#include <Servo.h> 

SoftwareSerial mySerial(9, 10);

 
int servoPin = 3; 
int data = 7;
String arr[] = {"9566072427","9790710035","9790712994","9790700998"};

 
Servo Servo1;


void setup()
{
  mySerial.begin(9600);   // Setting the baud rate of GSM Module  
  Serial.begin(9600);    // Setting the baud rate of Serial Monitor (Arduino)
  Servo1.attach(servoPin);
  delay(100);
}


void loop()
{
  if (Serial.available()>0)
  {
    data = Serial.read();
   if(data==0 || data==1 )
  {
    runMotor();
  }
  }

 if (mySerial.available()>0)
   Serial.write(mySerial.read());
}

 void runMotor()
 {
  Servo1.write(135);
  delay(1000);
  Servo1.write(55); 
  delay(5000);
  Servo1.write(135);
  for(int i = 0; i<4; i++)
  {
   SendMessage(arr[i]);
   delay(1000); 
    }
  
  }

 void SendMessage(String phone_number)
{
  mySerial.println("AT+CMGF=1");    //Sets the GSM Module in Text Mode
  delay(1000);  // Delay of 1000 milli seconds or 1 second
  String temp2 = String(phone_number);
  String temp = String("AT+CMGS=") + String("\"+91") + String(temp2) +"\""  + String("\r");
  mySerial.println(temp);
  delay(1000);
  mySerial.println("Your car has been identified and the amount has been deducted");// The SMS text you want to send
  delay(100);
   mySerial.println((char)26);// ASCII code of CTRL+Z
  delay(1000);
  
}

 
