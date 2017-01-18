#!/usr/bin/env python

import roslib; roslib.load_manifest('hmi_interpreter')
from hmi_interpreter.srv import *
from geometry_msgs.msg import *
from std_msgs.msg import *
import rospy
import re
import sys

import pygtk
pygtk.require('2.0')
import gtk
import string 
import os
import commands
from std_msgs.msg import String

def call_client(pose):
    string = String()
    string.data = "set"
    rospy.wait_for_service("pointing_server")
    try: 
        pointing_server = rospy.ServiceProxy("pointing_server", pointer)
        resp1 = pointing_server(string,pose)
        result = resp1.result
        return result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def subscriberCB(data):
    posy = data.pose
    result = call_client(posy)
    
def start_function():
    rospy.init_node("start_pointing_sub")
    rospy.Subscriber("busy_genius_left_hand", PoseStamped, subscriberCB)
    print "Ready for start_function with Subscriber"
    rospy.spin()



if __name__ == "__main__":
     start_function()
