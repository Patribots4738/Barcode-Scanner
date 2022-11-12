import cv2
from pyzbar import pyzbar
import time

cap = cv2.VideoCapture(1)

def decode(image):
    # returns the type and data of the first barcode it sees
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        return obj.type, obj.data
    return None, None

def write_to_csv(data):
	if not os.path.exists("log.csv"):
		with open ("log.csv", "w") as f:
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
	_, frame = cap.read()
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	cv2.imshow('img1', frame)  # display the captured image
	cv2.imshow('cropped', frame[200:280, 160:480])
	data = decode(frame)
	if data != (None, None): print(data, time.time())
	cv2.waitKey(1)
