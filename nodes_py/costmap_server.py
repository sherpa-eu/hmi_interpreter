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
from geometry_msgs.msg import Pose
from std_msgs.msg import String

object00="none"
def call_object_name(req):
    global object00
   
    if req.goal != "get":
        object00=req.goal
    return text_parserResponse(object00)

def get_costmap_server():
    rospy.init_node("add_costmap_server")
    msg = Pose()
    s = rospy.Service("add_costmap_name", text_parser, call_object_name)
    print "Ready to set the object name."
    rospy.spin()


if __name__ == "__main__":
    get_costmap_server()
