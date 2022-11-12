import cv2
from pyzbar import pyzbar
import time

#import dependencies
from ast import Index
from distutils.log import error
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
import numpy as np
import sys
# import board
# from neopixel import NeoPixel
import os

debug = True

cap = cv2.VideoCapture(1)

cache = {}

#----------------------------------------------------------------------------------------#
#connect to spreadsheet

# define the scope
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/adame/Github_Repositories/PatribotsSignIn/Barcode-Scanner/roboticsrfidsignin-99cdbd7ce58b.json", scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open("Test")

# get the  sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(2)

#get the log instance of the Spreadsheet
log_instance = sheet.get_worksheet(1)

if debug: print("connected to sheet")

#----------------------------------------------------------------------------------------#

def decode(image):
    # returns the type and data of the first barcode it sees
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        return obj.type, obj.data
    return None, None

def write_to_csv(data):
	if not os.path.exists("log.csv"):
		with open("log.csv", "w") as f:
			writer = csv.writer(f)
			writer.writerow(["Type", "Data"])
	
	with open("log.csv", "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

	# with open('barcode.csv', 'a', newline='') as file:
	# 	writer = csv.writer(file)
	# 	writer.writerow(["Type", "Data"])
	# 	for obj in decodedObjects:
	# 		writer.writerow([obj.type, strip_data(obj.data)])

def takeFrame(camera):
	_, frame = camera.read()
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	cropped = frame[200:280, 160:480]
	cv2.imshow('cropped', cropped)
	data = decode(cropped)
	if data != (None, None): print(data, time.time())
	cv2.waitKey(1)
	return cropped

def sendData(id, time):
    sheet_instance.update("A2:B2", [[int(id), int(time)*1000]])

#checks if the user is signing in or out
def isSignIn(id):
    log = np.genfromtxt("./log.csv", delimiter=",")
    for i in range(len(log)-1, -1, -1):
        try:
            if log[i][0] == id:
                if log[i][2] == 1:
                    return True
                else:
                    return False
        except IndexError as e:
            if debug: print(e)
            return True
    return True

def logID(id, is_sign_in):
    with open ("./log.csv", "a") as log:
        is_sign_in = 1 if is_sign_in else 0
        if debug: print(f"is_sign_in (in log): {is_sign_in}")
        log.write(str(id).strip() + "," + str(time.time()).strip() + "," + str(is_sign_in) + "\n")

def setLED(status):
	pass




#main event loop
while 1:
	data = decode(takeFrame(cap))
	if data[0] == None:
		pass
	elif data[0] != "CODE39":
		if debug: print("DATA CORRUPTED")
		
	else:
		id = data[1]
		# try:
		#check to see if the cooldown for an id has expired
		try:
			#check if the card has been scanned in the last 60 seconds
			if time.time() - cache[int(id)] < 10:
				if debug: print("id on cooldown")
				setLED("error")
				
			else:
				if debug: print("id not on cooldown")
				raise Exception("All is good, this is just to run the except")

		except Exception:
			#send data to spreadsheet
			sendData(id, time.time())
			if debug: print(f"Sent id {id} to spreadsheet")

			is_sign_in = isSignIn(int(id))

			#play the corresponding chime
			if is_sign_in:
				setLED("in")
				
			else:
				setLED("out")
				
			

			#log id to csv file
			logID(id, is_sign_in)
			time.sleep(0.25)
			if debug: print("logged id to csv")

			#update the cache
			cache[int(id)] = time.time()
			if debug: print("updated cache")

		# except Exception as e:
		# 	if debug: print(e)
			
		# 	setLED("error")

		# except ValueError:
			
		# 	setLED("error")
		# 	continue

		# except Exception as e:
		# 	# #Sets LED to fatal and saves the error to an error log for later debugging
		# 	exc_type, _, exc_tb = sys.exc_info()
		# 	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		# 	# with open("/errors.csv", "a") as errorLog:
		# 	# 	errorLog.write(str(exc_type) + "," + str(fname) + "," + str(exc_tb.tb_lineno) + "," + str(e) + "\n")
		# 	# setLED("fatal")
			
		# 	raise SystemExit(str(exc_type) + "," + str(fname) + "," + str(exc_tb.tb_lineno) + "," + str(e) + "\n")

#try:
	#if debug: print("#-----------------------------------------#")
#except KeyboardInterrupt:
#	setLED("off")