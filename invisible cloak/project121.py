import cv2
import numpy as np
import time

fourcc=cv2.VideoWriter_fourcc(*'XVID')
output_file=cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
cap=cv2.VideoCapture(0)
time.sleep(2)
bg=0

for i in range(60):
    ret, bg=cap.read()
    bg=np.flip(bg, axis=1)

while(cap.isOpened()):
    ret, img=cap.read()
    if not ret: 
        break
    img=np.flip(img, axis=1)
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    bg=cv2.resize(bg, (640, 480))
    img=cv2.resize(bg, (640, 480))

    lower_black=np.array([30, 30, 0])
    upper_black=np.array([104, 153, 70])
    mask=cv2.inRange(hsv, lower_black, upper_black)

    mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask=cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    res=cv2.bitwise_and(bg, bg, mask=mask)
    f=bg-res
    f=np.where(f == 0, img, f)

    final_output=cv2.addWeighted(res, 1, img, 1, 0)
    output_file.write(final_output)
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
