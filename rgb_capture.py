import zmq
import cv2
import time
import numpy as np

def rgb_cap(context):
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5555")

    cap = cv2.VideoCapture(0)
    time.sleep(1)

    rgb_pts = np.float32([ [290,200], [546,176], [317,480], [583,473] ])
    e_pts = np.float32([ [233,134], [443,134], [236,375], [445,372] ])

    M = cv2.getPerspectiveTransform(rgb_pts, e_pts)

    while True:
        ret, frame = cap.read()
        warped = cv2.warpPerspective(frame, M, (frame.shape[1], frame.shape[0]), flags=cv2.INTER_LINEAR)
        warped = warped[:-120,:-150,:]
        socket.send_pyobj(warped)
        print("Sent rgb frame")