import cv2
import sys
import pytesseract
import numpy as np
import csv
import mysql.connector
import subprocess
import datetime
import time
import serial


now = datetime.datetime.now()


if __name__ == '__main__':
	
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="Ajitesh",
	  passwd="Ajitesh56",
	  database="Tarp_project"
	)

	mycursor = mydb.cursor()

	mycursor.execute("SELECT * FROM Vehicles")
	myresult = mycursor.fetchall()
	imPath = "images/computer-vision.jpg"
	cap = cv2.VideoCapture(0)    
	config = ('-l eng --oem 1 --psm 3')
	number_plate = ''
	wallet_amt = 0
	user_time = ''
	FMT = '%Y-%m-%d %H:%M:%S'
	vehicle_type = ''

	def check_entry(number_plate):
		flag = 0
		
		for x in myresult:
			if (x[0] == number_plate):
				flag = 1
				break
			else:
				flag = 0
		  
		if (flag == 1):
			return 1
		else:
			return 0	

	def getUserTime(number_plate):
		t = ''
		for x in myresult:
			if (x[0] == number_plate):
				t = x[4]
				break
		return t						
					
	
	def getNumberPlate(number_plate):
		plate = ''
		for x in myresult:
			if(x[0] == number_plate):
				plate = x[2]
				break
		return plate

	def getVehicleType(number_plate):
		vehicle = ''
		for x in myresult:
			if(x[0] == number_plate):
				vehicle = x[2]
				break
		return vehicle

	def getWalletAmount(number_plate):
		wallet = 0
		for x in myresult:
			if(x[0] == number_plate):
				wallet = x[3]
				break
		return wallet


	while True:
		ret, image_np = cap.read()
		image_np_expanded = np.expand_dims(image_np, axis=0)
		text = pytesseract.image_to_string(image_np, config=config)
		cv2.imshow('TARP', cv2.resize(image_np, (800,600)))
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
		if text != '':
			number_plate = text.strip()
			if len(number_plate)==10:
				print(number_plate)
				print("\n")
				if(check_entry(number_plate)):
					#print("The vehicle exists") 
					mycursor.execute("SELECT * FROM Vehicles")
					myresult = mycursor.fetchall()
					user_time = getUserTime(number_plate)
					current_time = now.strftime("%Y-%m-%d %H:%M:%S")
					tdelta = now.strptime(str(current_time), FMT) - now.strptime(str(user_time), FMT)
					current_wallet_amt = 0
					if(tdelta.days>0):
						vehicle_type = getVehicleType(number_plate)
						if(vehicle_type == "Private"):
							current_wallet_amt = getWalletAmount(number_plate)
							if(current_wallet_amt >= 200):
								amt = current_wallet_amt - 200
								query = """Update Vehicles set Wallet_Balance = %s where Number_Plate = %s"""
								input = (amt, number_plate)
								mycursor.execute(query, input)
								mydb.commit()
								query = """Update Vehicles set Time_Stamp = %s where Number_Plate = %s"""
								input = (current_time, number_plate)
								mycursor.execute(query, input)
								mydb.commit()
								mycursor.execute("Select * from Vehicles")
								myresult = mycursor.fetchall()
								print("Amount has been deducted")
								print("The gate will open")
								subprocess.check_call(["python3", "testing_motor5.py"])
								break
								time.sleep(8)
							else:
								print("You dont have sufficinet amount")
								print("The gate will not be opened")
						if(vehicle_type == "Public"):
							query = """Update Vehicles set Time_Stamp = %s where Number_Plate = %s"""
							input = (current_time, number_plate)
							mycursor.execute(query, input)
							mydb.commit()
							mycursor.execute("Select * from Vehicles")
							myresult = mycursor.fetchall()
							print("It was a public vehicle so no amount has been deducted")
							print("The gate will open")
							time.sleep(8)
							subprocess.check_call(["python3", "testing_motor5.py"])
							break
						if(vehicle_type == "Transport"):
							current_wallet_amt = getWalletAmount(number_plate)
							if(current_wallet_amt >= 500):
								amt = current_wallet_amt - 500
								query = """Update Vehicles set Wallet_Balance = %s where Number_Plate = %s"""
								input = (amt, number_plate)
								mycursor.execute(query, input)
								mydb.commit()
								query = """Update Vehicles set Time_Stamp = %s where Number_Plate = %s"""
								input = (current_time, number_plate)
								mycursor.execute(query, input)
								mydb.commit()
								mycursor.execute("Select * from Vehicles")
								myresult = mycursor.fetchall()
								print("Amount has been deducted")
								print("The gate will open")
								subprocess.check_call(["python3", "testing_motor5.py"])
								time.sleep(15)								
								break
								
							else:
								print("You dont have sufficinet amount")
								print("The gate will not open")
							
					else:
						## OPEN THE GATE
						print("The gate will open")
						subprocess.check_call(["python3", "testing_motor5.py"])
						time.sleep(15)
						break	
				else:
					## DONOT OPEN THE GATE
					print("The vehicle doesnot exists")
					print("The gate will not open")

				

