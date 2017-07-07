#!/usr/bin/env python
 
from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
from std_msgs.msg import String
import rospy
from json_prolog import json_prolog
 
result=''
tmp=''
ref_agent=""
serv_result=""
serv_detector=""
publisher =''

def check_beacon_agent():
    global serv_result
    # check which agent a beacon has
    test=[]
    agent = ""
    prolog = json_prolog.Prolog()
    query = prolog.query("map_object_type(A,'http://knowrob.org/kb/knowrob.owl#Beacon'), owl_has(Robot,'http://knowrob.org/kb/srdl2-comp.owl#subComponent',A)")
    for solution in query.solutions():
        s = solution['Robot']
        test.append(s)
    query.finish()
    test = list(set(test))

    # service: check if agent is red wasp, if not send red wasp
    rospy.wait_for_service("add_agent_name")
    serv_result="Did not work!"
    try:
        add_agent_name = rospy.ServiceProxy("add_agent_name",text_parser)
        resp2 = add_agent_name("get")
        serv_result = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

    for i in test:
        if "Red" in i:
            if serv_result == "red_wasp":
                return "YES"
            else:
                return "NO"



def check_cam_agent():
    global serv_result
    global result

    # checking which agent has a cam
    test=[]
    prolog = json_prolog.Prolog()
    query = prolog.query("map_object_type(A,'http://knowrob.org/kb/srdl2-comp.owl#ColorCamera'), owl_has(Robot,'http://knowrob.org/kb/srdl2-comp.owl#subComponent',A)")
    for solution in query.solutions():
        test.append(solution['Robot'])
    query.finish()
    test=list(set(test))
    
    # checking if selected agent has a cam

    rospy.wait_for_service("add_agent_name")
    serv_result="Did not work!"
    try:
        add_agent_name = rospy.ServiceProxy("add_agent_name",text_parser)
        resp2 = add_agent_name("get")
        serv_result = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
        
    for i in test:
        if "Blue" in i or "Hawk" in i:
            if serv_result == "blue_wasp" or serv_result == "hawk":
                return "YES"
            else:
                return "NO"
        
        
def check_detected(value):
    rospy.wait_for_service("detector")
    serv_detector="Did not work!"
    try:
        add_agent_name = rospy.ServiceProxy("detector",text_parser)
        resp2 = add_agent_name(value)
        serv_detector = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
    if serv_detector == "YES":
        return "YES"
    else:
        return "NO"

# TODO: SHPW PICTURE

def agent_system(sentence):
    global tmp
    global result
    print "agent_system"
    detected = ""
    check_agent = ""
    if "take" in sentence and "picture" in sentence:
        if "kite" in sentence:
            check_agent =check_cam_agent()
            if check_agent == "YES":
                result = "BRAVO"
            else:
                result = "NIENTE"
                publisher.publish("This agent has no cam. Please continue the command with another agent!")
        elif "victim" in sentence:
            check_agent = check_cam_agent()
            if check_agent == "YES":
                result = "BRAVO"
            else:
                result = "NIENTE"
                publisher.publish("This agent has no cam. Please continue the command with another agent!")
        else:
            check_agent = check_cam_agent()
            if check_agent == "YES":
                result = "BRAVO"
            else:
                result = "NIENTE"
                publisher.publish("This agent has no cam. Please continue the command with another agent!")
    elif "search" in sentence:
        tmp = sentence
        if "kite" in sentence:
            check_agent = check_cam_agent()
            print "check_agent"
            print check_agent
            if check_agent == "YES":
                result = "BRAVO"
            else:
                result = "NIENTE"
                publisher.publish("This agent has no cam. Please continue the command with another agent!")
        elif "victim" in sentence:
            check_agent = check_beacon_agent()
            check_agent2 = check_cam_agent() 
            if check_agent == "YES":
                result = "BRAVO"
            elif check_agent2 == "YES":
                result = "BRAVO"
            else:
                result = "NIENTE"
                publisher.publish("This agent has no cam. Please continue the command with another agent!")
        else:
            result="NOCOMMAND"
    else:
        result = "NOCOMMAND"


def call_agent(req):
    print "Calling acms_checker"
    agent_system(req.goal)
    speech_output = result
    return text_parserResponse(speech_output)

def agent_checker():
    global publisher
    rospy.init_node("agent_caller")
    publisher = rospy.Publisher('display_command', String, queue_size=10)
    s = rospy.Service("acms_checker",text_parser,call_agent)
    print "Waiting for instruction to check acms"
    rospy.spin()

if __name__ == "__main__":
    agent_checker()
