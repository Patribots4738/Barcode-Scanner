#read barcode from image
import cv2
import pyzbar.pyzbar as pyzbar
import csv

def strip_data(data):
	value = str(data)[2:-1]
	return value

def collect_data(decodedList):
	for obj in decodedList:
	#remove the first two and last character
	#print Type and Data
		print('Type : ', obj.type)
		print('Data : ', strip_data(obj.data),'\n')
	return obj

def write_to_csv():
	with open('barcode.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Type", "Data"])
		for obj in decodedObjects:
			writer.writerow([obj.type, strip_data(obj.data)])

def show_image(image):
	cv2.imshow('Image', image)
	cv2.waitKey(0)

img = cv2.imread('./fix.png')

decodedObjects = pyzbar.decode(img)

data = collect_data(decodedObjects)

write_to_csv()
