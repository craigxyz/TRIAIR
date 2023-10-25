import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
time.sleep(1)

rgb_pts = np.float([ [], [], [], [], ])
e_pts = np.float([ [], [], [], [], ])

M = cv2.getPerspectiveTransform(rgb_pts, e_pts)

while True:
    ret, frame = cap.read()
    warped = cv2.warpPerspective(frame, M, (frame.shape[1], frame.shape[0]), flags=cv2.INTER_LINEAR)
    cv2.imshow('unwarp', frame)
    cv2.imshow('warped', warped)
    cv2.waitKey(1)