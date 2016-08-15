import numpy as np
import cv2

cap = cv2.VideoCapture(1)
num = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('i'+str(num)+'.jpg',frame)
        num = num + 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()