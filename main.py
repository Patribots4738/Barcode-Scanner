#read barcode from image
import cv2
import pyzbar.pyzbar as pyzbar

img = cv2.imread('./fix.png')

decodedObjects = pyzbar.decode(img)
for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')

cv2.imshow("Frame", img)
cv2.waitKey(0)

# Path: barcode.jpg
# Barcode image
