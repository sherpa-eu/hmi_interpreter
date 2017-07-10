#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
import rospy

result=''
  
def contexting(sentence):
    global result
    if sentence == "search that lake for kite" or sentence == "search that bridge for kite":
        rospy.wait_for_service("detector")
        result = "Did not work!"
        try:
            detector = rospy.ServiceProxy("detector",text_parser)
            resp2 = detector("kite")
            result = resp2.result
            return result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
            # look for kite, already detected?
            # look for victim, already detected?
    else:
        rospy.wait_for_service("detector")
        result = "Did not work!"
        try:
            detector = rospy.ServiceProxy("detector",text_parser)
            resp2 = detector("victim")
            result = resp2.result
            return result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e

def call_checker(req):
    print "Checking for Storing Value"
    speech_output = contexting(req.goal)
    #speech_output = result
    return text_parserResponse(speech_output)


def context_checker():
    rospy.init_node("context_checker")
    s = rospy.Service("context", text_parser, call_checker)
    print "Command collector is ready to store instructions!"
    rospy.spin()

if __name__== "__main__":
    context_checker()
