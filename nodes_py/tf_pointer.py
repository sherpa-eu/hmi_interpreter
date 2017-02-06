#!/usr/bin/env python  
import roslib
roslib.load_manifest('hmi_interpreter')
import rospy
import math
import tf
from geometry_msgs.msg import PoseStamped
import geometry_msgs.msg
import hmi_interpreter.srv

if __name__ == '__main__':
    rospy.init_node('tf_checker')

    listener = tf.TransformListener()
    pose = PoseStamped()
    rate = rospy.Rate(5.0)
    while not rospy.is_shutdown():
        try:
            (trans_right,rot_right) = listener.lookupTransform('/map', '/busy_genius/right_hand', rospy.Time(0))
            (trans_left,rot_left) = listener.lookupTransform('/map', '/busy_genius/left_hand', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        if trans_right[2] >= trans_left[2]:
            pose.pose.position.x = trans_right[0]
            pose.pose.position.y = trans_right[1]
            pose.pose.position.z = trans_right[2]
            pose.pose.orientation.x = rot_right[0]
            pose.pose.orientation.y = rot_right[1]
            pose.pose.orientation.z = rot_right[2]
            pose.pose.orientation.w = rot_right[3]
            print "right"
        else:
            pose.pose.position.x = trans_left[0]
            pose.pose.position.y = trans_left[1]
            pose.pose.position.z = trans_left[2]
            pose.pose.orientation.x = rot_left[0]
            pose.pose.orientation.y = rot_left[1]
            pose.pose.orientation.z = rot_left[2]
            pose.pose.orientation.w = rot_left[3]
            print "left"
        print pose
        
