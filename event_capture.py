import zmq
import numpy as np
import cv2

from metavision_core.event_io import EventsIterator
from metavision_sdk_core import BaseFrameGenerationAlgorithm, PeriodicFrameGenerationAlgorithm
from metavision_sdk_ui import EventLoop, Window

def event_cap(context):

    mv_iterator = EventsIterator(input_path="", delta_t=50000)
    height, width = mv_iterator.get_size()  # Camera geometry

    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5557")

    for evs in mv_iterator:
        image = np.zeros((height, width,3), dtype=np.uint8)
        BaseFrameGenerationAlgorithm.generate_frame(evs, image, accumulation_time_us=50000)
        image = image[:-145,:-150,:]
        socket.send_pyobj(image)