#!/usr/bin/env python

import roslib; roslib.load_manifest('hmi_interpreter')
from hmi_interpreter.srv import *
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

interest_object="no-elem"

def call_openEase(req):
    global interest_object
    if req.goal != "get":
        interest_object = req.goal
        return text_parserResponse(interest_object)
    else:
        tmp = interest_object
        interest_object = "no-elem"       
        return text_parserResponse(tmp)

def get_openEase_server():
    rospy.init_node("add_openEase_object_server")
    s = rospy.Service("add_openEase_object", text_parser, call_openEase)
    print "Ready for openease server."
    rospy.spin()


if __name__ == "__main__":
    get_openEase_server()
