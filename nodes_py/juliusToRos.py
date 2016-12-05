#!/usr/bin/env python

import socket
from subprocess import Popen
import multiprocessing
import rospy
import os
import string
from math import floor
from std_msgs.msg import String

def callJulius(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    print "port"
    print port
    p = Popen(['julius', '-C', '../julius_files/sherpa.jconf','-input','mic'], stdout= s, stderr= s)

def recognizer():
    pub = rospy.Publisher('/recognizer/output',String, queue_size=10)
    rospy.init_node('HRI_Recognizer')
    msg = String()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.listen(1)


    p = multiprocessing.Process(target=callJulius, args=(port,))
    p.start()
    conn, addr = s.accept()

    while not rospy.is_shutdown():
        data = conn.recv(4096)
        if data.find("sentence1") >= 0:
            data=data[data.find("sentence1")+15:data.find(" </s>")]
            msg.data = data
        
            
            pub.publish(msg)

    s.close()
    p.close()



if __name__ == '__main__':
    recognizer()
