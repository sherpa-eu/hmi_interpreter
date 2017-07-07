#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
import rospy

stack=[]
result=''
  

def detection_call(value):
    rospy.wait_for_service("detector")
    result = "Did not work!"
    try:
        detector = rospy.ServiceProxy("detector",text_parser)
        resp2 = detector(value)
        return resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e


def storing(sentence):
    global stack
    global result
    desig = Desig()
    sentence = sentence[0]
    if sentence.checker.data == "get":
        res = stack.pop()
        stack.append(res)
        result=res
        return result
    elif sentence.checker.data == "checked":
        res = stack.pop()
        stack.append(res)
        result=res
        print res
        if res.action_type.data == "take-picture" and res.actor.data == "blue_wasp":
            val = detection_call("victim")
            print "Ok let's be a bit proactive"
            print "val"
            print val
            if val == "YES":
                desig = Desig()
                desigs = []
                propkey = Propkey()
                propkeys = []
                desig.action_type.data = "go"
                desig.actor.data = "donkey"
                desig.instructor.data = "busy_genius"
                desig.viewpoint.data = "busy_genius"
                propkey.object_relation.data = "to"
                propkey.object.data = "victim"
                propkeys.append(propkey)
                desig.propkeys = propkeys
                stack.append(desig)
                desigs.append(desig)
                print "cram"
                print desigs[0]
                rospy.wait_for_service("service_hmi_cram")
                result = "Did not work!"
                try:
                    service_hmi_cram = rospy.ServiceProxy("service_hmi_cram",HMIDesig)
                    resp2 = service_hmi_cram(desigs)
                    tmp = resp2.result
                    print tmp
                    return tmp
                except rospy.ServiceException, e:
                    print"Service call failed: %s"%e
            else:
                return "Victim not detected. No proactive behavior"

        else:
            return "Okay no proactive behavior"
    else:
     desig.action_type.data = sentence.action_type.data
     desig.actor.data = sentence.actor.data
     desig.instructor.data= sentence.instructor.data
     desig.viewpoint.data= sentence.viewpoint.data
     desig.propkeys = sentence.propkeys
     result = desig
     stack.append(desig)
     return result
     

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
