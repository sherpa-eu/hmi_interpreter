#!/usr/bin/env python

import socket
from subprocess import Popen
import multiprocessing
import rospy
import os
import string
from hmi_interpreter.srv import text_parser
from math import floor
from std_msgs.msg import String
import rospkg
import sys 


path=''
server_address=('localhost', 10000)
p=''
s=''
num=0

def callJulius(port):
    global p
    global s
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(('127.0.0.1', port))
    s.settimeout(None)
    p = Popen(['julius', '-C',rospack.get_path('hmi_interpreter')+'/julius_files/sherpa.jconf','-input','mic'], stdout= s, stderr= s)

def call_my_julius(req):
    print "call my julius "
    #if req.goal == "true":
    req.goal = "true"
    recognize(req.goal)
    #s.shutdown(socket.SHUT_RDWR)
    #s.close()      
    
    return "false"
        
def recognize(req):
    global s
    global p
    global num
    global conn
    global port
    msg = String()
    pub = rospy.Publisher('/recognizer/output',String, queue_size=10)
    if num == 0:
        # rospy.init_node('HRI_Recognizer')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "socket"
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        print port
        s.listen(1)
        p = multiprocessing.Process(target=callJulius, args=(port,))
        p.start()
        conn, addr = s.accept()
        num = 1
        print "....................................."
    while not rospy.is_shutdown():
        data = conn.recv(4096)
        print "---data---"
        print data
        if data.find("sentence1") >= 0:
            print "teest123"
            print data
            data=data[data.find("sentence1")+15:data.find(" </s>")]
            if data == "GO A HEAD":
                data = "GO AHEAD"
            elif data == "GOLEFT":
                data = "GO LEFT"
            elif data == "GO TO HELI PAD":
                data = "GO TO HELIPAD"
                print "hier"
                print data
            elif data == "LAND AT HELI PAD":
                data = "LAND AT HELIPAD"
            elif data == "GO TO COT TA GE":
                data = "GO TO COTTAGE"
            elif data == "SEARCH THAT LAKE VICTIM":
                data = "SEARCH THAT LAKE FOR VICTIM"
            elif data == "SEARCH THAT LAKE KITE":
                data = "SEARCH THAT LAKE FOR KITE"
            elif data == "SEARCH THAT BRIDGE VICTIM":
                data = "SEARCH THAT BRIDGE FOR VICTIM"
            elif data == "SEARCH THAT BRIDGE KITE":
                data = "SEARCH THAT BRIDGE FOR KITE"
            elif data == "SEARCH THAT AREA VICTIM":
                data = "SEARCH THAT AREA FOR VICTIM"
            elif data == "SEARCH THAT AREA KITE":
                data = "SEARCH THAT AREA FOR KITE"
            elif data == "UN MOUNT RED WASP":
                data = "UNMOUNT RED WASP"
            elif data == "UN MOUNT BLUE WASP":
                data = "UNMOUNT BLUE WASP"
            else:
                data = data
                print data
                print "-a-a-a-data-a-a-a-"
                print data
            msg.data = data
            pub.publish(msg)
    print p
    return "false"

def recognizer_server():
    rospy.init_node('julius_starter')
    s = rospy.Service('julius_server', text_parser, call_my_julius)
    rospy.spin()
 

if __name__ == '__main__':
    print "start main julius "
    rospack = rospkg.RosPack()
    path = rospack.get_path('hmi_interpreter')
    recognizer_server()
