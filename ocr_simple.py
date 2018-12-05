import cv2
import sys
import pytesseract
import numpy as np
import csv
import mysql.connector
import subprocess


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
	private_vehicle = 200
	public_vehicle = 0
	transport_vehicle = 500
	flag = 0
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
			if len(number_plate)==9:
				print(number_plate)
				print("\n")
				for x in myresult:
					if number_plate == x[0]:
						wallet_amt = x[3]
						if x[2] == 'Private' and wallet_amt>200
							wallet_amt = wallet_amt - 200						
							break
						else:
							flag = 1
							break
						if x[2] == 'Public' 
							wallet_amt = wallet_amt
							break
						else:
							flag = 2
							break
						if x[2] == 'Transport' and wallet_amt>500
							wallet_amt = wallet_amt - 500
						else:
							flag = 3
							break
				if flag == 1 or flag == 2 or flag == 3:
					print("The user is authorised to pass \n")
					print("The amount has been deducted\n")
					sql = "UPDATE Vehicles SET Wallet_Balance = %s WHERE Number_Plate = %s"
					val = (wallet_amt, number_plate)
					mycursor.execute(sql, val)
					mydb.commit()
					subprocess.check_call(["python3", "testing_motor5.py"])
				else
					print("You Dont have sufficient amount in your wallet please pay manually")
						
						
				
			

