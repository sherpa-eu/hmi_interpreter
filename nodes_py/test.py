#!/usr/bin/env python  
import roslib
roslib.load_manifest('hmi_interpreter')
import rospy
import math
import tf
import geometry_msgs.msg
import hmi_interpreter.srv

if __name__ == '__main__':
    rospy.init_node('tf')
    print "MOVE RIGHT"
    result = "MOVE RIGHT"
    result = result.split("MOVE")
    print result[0]
    print result[1]
