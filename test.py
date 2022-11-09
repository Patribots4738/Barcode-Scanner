#read barcode from laptop camera
import cv2
#inport numpy
import numpy as np
import pyzbar.pyzbar as pyzbar

cap = cv2.VideoCapture(2)

while True:
    _, frame = cap.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #change the frame to 1280x720z
    frame = cv2.resize(frame, (1280, 720))

    decodedObjects = pyzbar.decode(frame)
    # print(decodedObjects)
    #if len(decodedObjects) > 0 then print the data and break
    if len(decodedObjects) > 0:
        for obj in decodedObjects:
            print('Type : ', obj.type)
            print('Data : ', obj.data, '\n')
        break
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

