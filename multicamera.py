import zmq
import cv2	
from threading import Thread
from multiprocessing import Process
import os
import time

from rgb_capture import rgb_cap
from thermal_capture import thermal_cap
from event_capture import event_cap

rgb = None
ir = None
e = None

context = zmq.Context()

def all_recv():
    rgb_recv = context.socket(zmq.PULL)
    rgb_recv.connect("tcp://localhost:5555")

    ir_recv = context.socket(zmq.PULL)
    ir_recv.connect("tcp://localhost:5556")
    
    e_recv = context.socket(zmq.PULL)
    e_recv.connect("tcp://localhost:5557")

    # get some folder structure in place
    top_level_folder = '3_cam_data'
    if not os.path.exists(top_level_folder):
        os.mkdir(top_level_folder)

    # make a folder for this session
    session_name = str(time.time())
    os.mkdir(top_level_folder + '/' + session_name)
    
    class rgbThread(Thread):
    
        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.start()
    
        def run(self):
            global rgb
            while True:
                rgb = rgb_recv.recv_pyobj()

    class irThread(Thread):

        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.start()

        def run(self):
            global ir
            while True:
                ir = ir_recv.recv_pyobj()

    class eThread(Thread):

        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.start()

        def run(self):
            global e
            while True:
                e = e_recv.recv_pyobj()

    class displayThread(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.start()

        def run(self):
            count = 0
            while True:
                
                print('rgb', type(rgb))
                print('ir', type(ir))
                print('e', type(e))

                if rgb is None or ir is None or e is None:
                    continue

                cv2.imshow('crgb', rgb)
                cv2.imwrite(top_level_folder + '/' + session_name + '/rgb_' + session_name + '_' + str(count) + '.jpg', rgb)
                cv2.imshow('cir', ir)
                cv2.imwrite(top_level_folder + '/' + session_name + '/ir_'+session_name+'_'+str(count)+ '.jpg', ir)
                cv2.imshow('ce', e)
                cv2.imwrite(top_level_folder + '/' + session_name + '/e_'+session_name+'_'+str(count) + '.jpg', e)
                cv2.waitKey(1)
                count += 1



    rgbThread()
    irThread()
    eThread()
    displayThread()
    while True:
        pass
    


def main():
    p1 = Process(target=rgb_cap, args=(context, ))
    p2 = Process(target=thermal_cap, args=(context,))
    p3 = Process(target=event_cap, args=(context,))
    p4 = Process(target=all_recv, args=())

    p1.start()
    p2.start()
    p3.start()
    p4.start()

if __name__ == '__main__':
    main()