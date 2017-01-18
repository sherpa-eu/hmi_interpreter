#!/usr/bin/env python

from hmi_interpreter.srv import *
from geometry_msgs.msg import *
import rospy
import sys

pose=Pose()

def set_pointer(req):
    global pose
   
    print "Returning: "
    print req
    multi = req.pointing
    if req.action.data == "set" or req.action.data == "add":
        pose.position.x = multi.pose.position.x
        pose.position.y = multi.pose.position.y
        pose.position.z = multi.pose.position.z
        pose.orientation.x = multi.pose.orientation.x
        pose.orientation.y = multi.pose.orientation.y
        pose.orientation.z = multi.pose.orientation.z
        pose.orientation.w = multi.pose.orientation.w
        print "pose: "
        print pose
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
