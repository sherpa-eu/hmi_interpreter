#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
from std_msgs.msg import String
import rospy



def starting_cmd_collector_client(hmidesig):
    rospy.wait_for_service("cmd_collector")
    print "inside cmd_collector"
    print hmidesig
    try: 
        cmd_collector = rospy.ServiceProxy("cmd_collector", HMISTOREDesig)
        resp1 = cmd_collector(hmidesig)
        return resp1.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def subscriberCB(goal):
    storedesig = STOREDesig()
    hmidesig = []
    storedesig.checker.data = goal.data
    hmidesig.append(storedesig)
    print "subscriber of cmd_collector"
    print starting_cmd_collector_client
    starting_cmd_collector_client(hmidesig)


def start_checking_command():
    rospy.init_node("checking_cmd_collector")
    rospy.loginfo("Checking the instruction in order to be proactive")
    rospy.Subscriber("/check_cmd_collector", String, subscriberCB)
    print "Ready for check_cmd_collector"
    rospy.spin()

if __name__ == "__main__":
     start_checking_command()
