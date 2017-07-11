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


def storing(sentencer):
    global stack
    global result
    desig = Desig()
    sentence = sentencer[0]
    if sentence.checker.data == "get":
        if not stack:
            return "empty list"
        res = stack.pop()
        stack.append(res)
        result=res
        return "Done"
    elif sentence.checker.data == "checked":
        if not stack:
            return "empty list"
        res = stack.pop()
        stack.append(res)
        result=res
        if res.action_type.data == "take-picture" and res.actor.data == "blue_wasp":
         #   print  res.propkeys[0].object.data
            if res.propkeys[0].object.data == "kite":
                val = detection_call("kite")
            else:
                val = detection_call("victim")
            if val == "YES":
                desig = Desig()
                desigs = []
                propkey = Propkey()
                propkeys = []
                desig.action_type.data = "go"
                desig.actor.data = "donkey"
                desig.instructor.data = "ACMS"
                desig.viewpoint.data = "busy_genius"
                propkey.object_relation.data = "to"
                propkey.object.data = res.propkeys[0].object.data
                propkeys.append(propkey)
                desig.propkeys = propkeys
                stack.append(desig)
                desigs.append(desig)
                rospy.wait_for_service("service_proactivity")
                result = "Did not work!"
                try:
                    service_proactivity = rospy.ServiceProxy("service_proactivity",HMIDesig)
                    resp2 = service_proactivity(desigs)
                    tmp = resp2.result
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
        return "Done"
     

def call_collector(req):
    print "Checking for Storing Value"
    speech_output = storing(req.desigs)
    #speech_output = result
    return HMISTOREDesigResponse(speech_output)


def command_collector():
    rospy.init_node("command_collector")
    s = rospy.Service("cmd_collector", HMISTOREDesig, call_collector)
    print "Command collector is ready to store instructions!"
    rospy.spin()

if __name__== "__main__":
    command_collector()
