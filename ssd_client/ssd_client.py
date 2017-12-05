import zmq
import ssd_server_pb2
import cv2
import sys
import os
import time
import socket
import numpy as np

class SsdZmqClient:
    def __init__(self, server, timeout=10000):
        self.timeout = timeout
        self.server = server
        self.socket = None
        self.ctx = zmq.Context()
        self.hostname = socket.gethostname()
        self.pid = os.getpid()

    def detect(self, image):
        img = cv2.imread(image)
        img_encode = cv2.imencode('.jpg', img)[1]
        data_encode = np.array(img_encode)
        
        req = ssd_server_pb2.Request()
        req.id = self.get_request_id()
        req.data = data_encode.tostring()
           
        rep = self.do_request(req)
        if rep is None or rep.biz_code != 0:
            print("do_request error")
            return None
        if rep.biz_result is None or len(rep.biz_result)==0:
            return None
        print rep.compute_time,len(rep.biz_result)
        result = []
        for detection in rep.biz_result:
            result.append(
                    [detection.name,
                    detection.prob,
                    detection.left,
                    detection.top,
                    detection.right,
                    detection.bottom])
        return result
        
    def get_request_id(self):
        return '_'.join([self.hostname, str(self.pid), str(time.time())])

    def get_client_id(self):
        return self.get_request_id()

    def get_socket(self, reconnect = False):
        if reconnect:
            self.socket = None
        if self.socket is None:
            self.socket = self.ctx.socket(zmq.DEALER)
            self.socket.setsockopt(zmq.IDENTITY, self.get_client_id())
            self.socket.connect(self.server)
        return self.socket

    def do_request(self, req):
        socket = self.get_socket()
        if socket is None:
            print("create socket failed")
            return None
        socket.send(req.SerializeToString())
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        msgs = dict(poll.poll(self.timeout))
        if not (socket in msgs and msgs[socket] == zmq.POLLIN):
            print("timeout")
            return None
        rep_buf = socket.recv()
        if len(rep_buf)<=0:
            return None
        rep = ssd_server_pb2.Response()
        rep.ParseFromString(rep_buf)
        return rep


