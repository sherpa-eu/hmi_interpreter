#!/usr/bin/env python

from hmi_interpreter.srv import *
from geometry_msgs.msg import Pose
import rospy
import sys

pose=Pose()

def set_pointer(req):
    global pose
   
    print "Returning: "
    multi = req.pointing
    if req.action.data == "set":
        pose.position.x = multi.position.x
        pose.position.y = multi.position.y
        pose.position.z = multi.position.z
        pose.orientation.x = multi.orientation.x
        pose.orientation.y = multi.orientation.y
        pose.orientation.z = multi.orientation.z
        pose.orientation.w = multi.orientation.w
    else:
        print pose
    return pointerResponse(pose)

def add_pointing_server():
    rospy.init_node('add_pointing_server')
    s = rospy.Service('pointing_server', pointer, set_pointer)
    print "Ready to add pointing gesture."
    rospy.spin()

def handle_add_three_ints(req):
    print "Returning: "
    print req
    return text_parserResponse("test done2")


if __name__ == "__main__":
    add_pointing_server()
