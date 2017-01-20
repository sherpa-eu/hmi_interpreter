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

def call_client(data):
    rospy.wait_for_service("add_openEase_object")
    try: 
        add_openEase_object = rospy.ServiceProxy("add_openEase_object", text_parser)
        resp1 = add_openEase_object(data.data)
        result = resp1.result
        return result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def subscriberCB(data):
    result = call_client(data)
    
def start_function():
    rospy.init_node("start_openEase_sub")
    rospy.Subscriber("/openease_object", String, subscriberCB)
    print "Ready for openease start_function with Subscriber"
    rospy.spin()



if __name__ == "__main__":
     start_function()
