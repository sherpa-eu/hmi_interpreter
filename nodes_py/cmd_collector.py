#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
import rospy

stack=[]
result=''
  
def storing(sentence):
    global stack
    global result
    desig = Desig()
    sentence = sentence[0]
    if sentence.checker.data == "get":
        res = stack.pop()
        stack.append(res)
        result=res
    else:
     desig.action_type.data= sentence.action_type.data
     desig.actor.data= sentence.actor.data
     desig.instructor.data= sentence.instructor.data
     desig.viewpoint.data= sentence.viewpoint.data
     desig.propkeys = sentence.propkeys
     result = desig
     stack.append(desig)

def call_collector(req):
    print "Checking for Storing Value"
    storing(req.desigs)
    speech_output = result
    return HMISTOREDesigResponse(speech_output)


def command_collector():
    rospy.init_node("command_collector")
    s = rospy.Service("cmd_collector", HMISTOREDesig, call_collector)
    print "Command collector is ready to store instructions!"
    rospy.spin()

if __name__== "__main__":
    command_collector()
