#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
import time
from hmi_interpreter.msg import LogInfo
import sys

desigs = ""
pose  = ""
pub =''
pub_speaker = ''
agent00 = ""
saver=""
publisher=''
prev_command=""
hmidesig =""

def call_transparency_logging(cmd, executable, agent, objName, found):

    if agent == "":
        rospy.wait_for_service("add_agent_name")
        agent="Did not work!"
        try:
            add_agent_name = rospy.ServiceProxy("add_agent_name",text_parser)
            resp2 = add_agent_name("get")
            agent = resp2.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
    
    print "here"

    hascap = ''
    needcap = ''
    if agent == "blue-wasp" or agent == "blue wasp" or agent == "blue_wasp" or agent == "hawk":
        hascap = 'http://knowrob.org/kb/srdl2-comp.owl#ColorCamera'
    elif agent == "red-wasp" or agent == "red wasp" or agent == "red_wasp":
        hascap = 'http://knowrob.org/kb/knowrob.owl#Beacon'
        needcap = 'http://knowrob.org/kb/srdl2-comp.owl#ColorCamera'
    elif agent == "donkey":
        hascap = 'http://knowrob.org/kb/knowrob.owl#ChargingBattery'
        needcap = 'http://knowrob.org/kb/srdl2-comp.owl#ColorCamera'
        
    command = String()
    command.data = cmd
    executability = String()
    executability.data = executable
    agency = String()
    agency.data = agent
    needCap = String()
    needCap.data = needcap
    giveCap = String()
    giveCap.data = hascap
    objectName = String()
    objectName.data = objName
    foundObj = String()
    foundObj.data = found

    rospy.wait_for_service("logging_detection")
    serv_result = "Did not work logging detection!"
    try:
        logging_detection = rospy.ServiceProxy("logging_detection", logging_detector)
        resp3 = logging_detection(command, executability, agency, needCap, giveCap, objectName, foundObj)
        return resp3.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

                    


def create_hmi_msgs(goal, agent, viewpoint, pose, openEase):
    global desigs
    global hmidesig
    desig = Desig()
    storedesig = STOREDesig()
    desigs = []
    hmidesig = []
    goal = goal.split(" 0 ")
    propkey = Propkey()
    propkey2 = Propkey()
    propkeys = []
    point = Point()
    if len(goal) == 1:
        goal = goal[0].split(" 1 ")
        if len(goal) == 1:                                 #Go to tree
            goal = goal[0].split(" ")
            storedesig.action_type.data = goal[0]
            desig.action_type.data = goal[0]
            storedesig.actor.data = agent
            desig.actor.data = agent
            storedesig.instructor.data = "busy_genius"
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
                storedesig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
                storedesig.viewpoint.data = "busy_genius"
            propkey.object_relation.data = goal[1]
            propkey.object.data = goal[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal[3]
            if goal[3] == "true" and goal != "there" and openEase != "none":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w
            
            propkeys.append(propkey)
            propkey = Propkey()
            desig.propkeys = propkeys
            storedesig.propkeys = propkeys
            desigs.append(desig)
            hmidesig.append(storedesig)
        else:
            goal1 = goal[0].split(" ")                    #Go to tree to rock
            storedesig.action_type.data = goal1[0]
            desig.action_type.data = goal1[0]
            storedesig.actor.data = agent
            desig.actor.data = agent
            storedesig.instructor.data = "busy_genius"
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
                storedesig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
                storedesig.viewpoint.data = "busy_genius"
            propkey.object_relation.data = goal1[1]
            propkey.object.data = goal1[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal1[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal1[3]
            if goal1[3] == "true" and goal != "there" and openEase != "none":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w

            propkeys.append(propkey)
            propkey = Propkey()
            goal2 = goal[1].split(" ")
            propkey.object_relation.data = goal2[0]
            propkey.object.data = goal2[3]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal2[1]
            propkey.object_num.data = "null"
            propkey.flag.data = goal2[2]
            if goal2[2] == "true" and goal != "there" and openEase != "none":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w
            propkeys.append(propkey)
            propkey = Propkey()
            propkeys.reverse()
            desig.propkeys = propkeys
            storedesig.propkeys = propkeys
            desigs.append(desig)
            hmidesig.append(storedesig)
            desig = Desig()
            storedesig = STOREDesig()
    else:   
        goal1 = goal[0].split(" 1 ")
        if len(goal1) == 1:  
            goal1 = goal1[0].split(" ")                                 #Go to tree
            desig.action_type.data = goal1[0]
            storedesig.action_type.data = goal1[0]
            desig.actor.data = agent
            storedesig.actor.data = agent
            desig.instructor.data = "busy_genius"
            storedesig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
                storedesig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
                storedesig.viewpoint.data = "busy_genius"
            propkey.object_relation.data = goal1[1]
            propkey.object.data = goal1[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal1[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal1[3]
            if goal1[3] == "true" and goal != "there" and openEase != "none":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w
            propkeys.append(propkey)
            desig.propkeys = propkeys
            storedesig.propkeys = propkeys
            desigs.append(desig)
            hmidesig.append(storedesig)
            desig = Desig()
            storedesig = STOREDesig()
        else:
            goal3 = goal1[0].split(" ")                                             #Go right to tree
            desig.action_type.data = goal3[0]
            storedesig.action_type.data = goal3[0]
            desig.actor.data = agent
            storedesig.actor.data = agent
            desig.instructor.data = "busy_genius"
            storedesig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
                storedesig.viewpoint.data = agent

            else:
                desig.viewpoint.data = "busy_genius"
                storedesig.viewpoint.data = "busy_genius"
         
            propkey.object_relation.data = goal3[1]
            propkey.object.data = goal3[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal3[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal3[3]
            if goal3[3] == "true" and goal != "there" and openEase != "none":
                propkey.object.data = openEase
            propkey.pointing_gesture.x = pose.position.x
            propkey.pointing_gesture.y = pose.position.y
            propkey.pointing_gesture.z = pose.position.z
            propkeys.append(propkey)
            propkey = Propkey()
            goal2 = goal1[1].split(" ")
            propkey.object_relation.data = goal2[0]
            propkey.object.data = goal2[3]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal2[1]
            propkey.object_num.data = "null"
            propkey.flag.data = goal2[2]
            if goal2[2] == "true" and goal != "there" and openEase != "none":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w
            propkeys.append(propkey)
            propkeys.reverse()
            desig.propkeys = propkeys
            storedesig.propkeys = propkeys
            desigs.append(desig)
            hmidesig.append(storedesig)
            desig = Desig()
            storedesig = STOREDesig()

        goal2 = goal[1].split(" 1 ")
        if len(goal2) == 1:                                                    #take-picture
            goal2 = goal2[0].split(" ")
            desig.action_type.data = goal2[0]
            storedesig.action_type.data = goal2[0]
            desig.actor.data = agent
            storedesig.actor.data = agent
            desig.instructor.data = "busy_genius"
            storedesig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
                storedesig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
                storedesig.viewpoint.data = "busy_genius"
            propkey = Propkey()
            propkey.object_relation.data = goal2[1]
            propkey.object.data = goal2[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal2[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal2[3]
            if goal2[3] == "true" and goal != "there" and openEase != "none":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w
            propkeys = []
            propkeys.append(propkey)
            desig.propkeys = propkeys
            storedesig.propkeys = propkeys
            desigs.append(desig)
            hmidesig.append(storedesig)
            desig = Desig()
            storedesig = STOREDesig()
            propkeys = []
        else:                                                              #take picture to rock
            goal1 = goal2[0].split(" ")
            desig = Desig()
            storedesig = STOREDesig()
            propkey = Propkey()
            propkey2 = Propkey()
            propkeys = []
            desig.action_type.data = goal1[0]
            storedesig.action_type.data = goal1[0]
            desig.actor.data = agent
            storedesig.actor.data = agent
            desig.instructor.data = "busy_genius"
            storedesig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
                storedesig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
                storedesig.viewpoint.data = "busy_genius"
            propkey2.object_relation.data = goal1[1]
            propkey2.object.data = goal1[4]
            propkey2.object_color.data = "null"
            propkey2.object_size.data = goal1[2]
            propkey2.object_num.data = "null"
            propkey2.flag.data = goal1[3]
            if goal1[3] == "true" and goal != "there":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w
            propkeys.append(propkey2)
            propkey2 = Propkey()
            propkeys2 = []
            goal4 = goal2[1].split(" ")
            #print "goal4"
            #print goal4
            propkey2.object_relation.data = goal4[0]
            propkey2.object.data = goal4[3]
            propkey2.object_color.data = "null"
            propkey2.object_size.data = goal4[1]
            propkey2.object_num.data = "null"
            propkey2.flag.data = goal4[2]
            if goal4[2] == "true" and goal != "there":
                propkey.object.data = openEase
            propkey.pointing_gesture.position.x = pose.position.x
            propkey.pointing_gesture.position.y = pose.position.y
            propkey.pointing_gesture.position.z = pose.position.z
            propkey.pointing_gesture.orientation.x = pose.orientation.x
            propkey.pointing_gesture.orientation.y = pose.orientation.y
            propkey.pointing_gesture.orientation.z = pose.orientation.z
            propkey.pointing_gesture.orientation.w = pose.orientation.w
            propkeys.append(propkey2)
            propkeys.reverse()
            desig.propkeys = propkeys
            storedesig.propkeys= propkeys
            desigs.append(desig)
            hmidesig.append(storedesig)
            desig = Desig()
            storedesig = STOREDesig()
    
   # print desigs
    
def go_into_collector(hmidesig):
    rospy.wait_for_service("cmd_collector")
    serv_result = "Did not work cmd_collector!"
    try:
        cmd_collector = rospy.ServiceProxy("cmd_collector", HMISTOREDesig)
        resp3 = cmd_collector(hmidesig)
        return resp3.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

def call_second_server(req):
    global agent00
    print "call_second_server"
    rospy.wait_for_service("ros_parser")
    result = "Did not work!"
    print "waiting for parsr"
    try:
        ros_parser = rospy.ServiceProxy("ros_parser",text_parser)
        resp1 = ros_parser(req)
        result = resp1.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
    
    rospy.wait_for_service("add_agent_name")
    agent = "Did not work!"
    print "waiting for agent name"
    try:
        add_agent_name = rospy.ServiceProxy("add_agent_name",text_parser)
        resp2 = add_agent_name("get")
        agent = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

    agent00 = agent
    rospy.wait_for_service("start_bg_logging")
    bg = "Did not work!"
    print agent00
    print "waiting for logging"
    try:
        start_bg_logging = rospy.ServiceProxy("start_bg_logging",log_info)
        goal = LogInfo()
        end2 = rospy.Time.from_sec(time.time()) # rospy.Time.now()
        t = end2.to_sec()
        end = t
        goal.timer=str(end)
        goal.agent=agent00
        goal.cmd=req
        goal.commander = "busy_genius"
        resp3 = start_bg_logging(goal)
        bg = resp3.result
        ##     create_hmi_msgs(resp1.result)
        ##     GENERATE the CRAM CLIENT
        ##     return "Okay everything went well"
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
        
    rospy.wait_for_service("add_viewpoint")
    viewpoint = "Did not work!"
    print "waiting for viewpoint"
    try:
        add_viewpoint = rospy.ServiceProxy("add_viewpoint",text_parser)
        resp2 = add_viewpoint("get")
        viewpoint = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

    rospy.wait_for_service("pointing_server")
    pose = "Did not work!"
    print "waiting for pointing server"
    try:
        pointing_server = rospy.ServiceProxy("pointing_server",pointer)
        string = String()
        posy = PoseStamped()
        string.data = "get"
        resp2 = pointing_server(string,posy)
        posy = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
    
    rospy.wait_for_service("add_openEase_object")
    pose = "Did not work!"
    print "openease object"
    try:
        add_openEase_object = rospy.ServiceProxy("add_openEase_object",text_parser)
        string = String()
        string.data = "get"
        resp2 = add_openEase_object("get")
        openEase = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
  
    print "go into create desigs method"
    print req
    print agent
    call_transparency_logging(req, "yes",agent,"", "")
    create_hmi_msgs(resp1.result, agent, viewpoint, posy,openEase)
    print agent
    pub.publish(desigs[0])
    rate = rospy.Rate(20)
    valy = go_into_collector(hmidesig)
    rospy.wait_for_service("service_hmi_cram")
    print "waiting for cram service"
    try:
        service_hmi_cram = rospy.ServiceProxy("service_hmi_cram",HMIDesig)
        resp2 = service_hmi_cram(desigs)
        tmp = resp2.result
        
        time.sleep(5)
        pub_speaker.publish("done")
        return tmp
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e


def checking_agent(value):
    print "checking agent"
    if "kite" in value:
        rospy.wait_for_service("acms_checker")
        serv_checker = "Did not work!"
        try:
            acms_checker = rospy.ServiceProxy("acms_checker",text_parser)
            resp1 = acms_checker(value)
            return resp1.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
    elif "victim" in value:
        rospy.wait_for_service("acms_checker")
        serv_checker = "Did not work!"
        try:
            acms_checker = rospy.ServiceProxy("acms_checker",text_parser)
            resp1 = acms_checker(value)
            return resp1.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
    elif "picture":
        rospy.wait_for_service("acms_checker")
        serv_checker = "Did not work!"
        try:
            acms_checker = rospy.ServiceProxy("acms_checker",text_parser)
            resp1 = acms_checker(value)
            return resp1.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
    else:
        return "NOCOMMAND"

def check_yes_no_command (value,prev):
    print "check yes no command"
    # if "victim" in prev:
    #     pvalue = "victim"
    # elif "kite" in prev:
    #     pvalue = "kite"
    if value == "yes" and prev != "" and prev != "yes" and prev != "no":
        publisher.publish(prev)
      #  call_transparency_logging(prev, "no","", pvalue, "yes")
        call_second_server(prev)
        # if command is yes but prev command not given
    elif value == "yes" and prev == "":
        publisher.publish("Please repeat your instruction!")
        return "nix"
        # of command is No
    elif value == "no":
        publisher.publish("Waiting for new instruction.")
       # call_transparency_logging(prev, "no","", pvalue, "yes")
        return "nix"

def check_search_command (value, prev):
    print "check search command"
    if "victim" in value:
        rospy.wait_for_service("detector")
        detector_goal = "Did not work!"
        try:
            detector = rospy.ServiceProxy("detector",text_parser)
            resp1 = detector("victim")
            detector_goal = resp1.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
      
        if detector_goal == "YES":
            publisher.publish("Victim already found. Continue searching, yes or no?")
            call_transparency_logging(value, "no","", "victim", "yes")
            return "nix"
        else:
            call_second_server(value)
    elif "kite" in value:
        rospy.wait_for_service("detector")
        detector_goal = "Did not work!"
        try:
            detector = rospy.ServiceProxy("detector",text_parser)
            resp1 = detector("kite")
            detector_goal = resp1.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
      
        if detector_goal == "YES":
            publisher.publish("Kite already found. Continue searching, yes or no?")
            call_transparency_logging(value, "no","", "kite", "yes")
            return "nix"
        else:
            call_second_server(value)
    else:
        if prev != "" and prev != "yes" and prev != "no":
                if "victim" in prev:
                    rospy.wait_for_service("detector")
                    detector_goal = "Did not work!"
                    try:
                        print "testedadr123789"
                        detector = rospy.ServiceProxy("detector",text_parser)
                        resp1 = detector("victim")
                        detector_goal = resp1.result
                    except rospy.ServiceException, e:
                        print"Service call failed: %s"%e
                    if detector_goal == "YES":
                        publisher.publish("Victim already found. Continue searching, yes or no?")
                        call_transparency_logging(prev, "no","", "victim", "yes")
                        return "nix"
                    else:
                        call_second_server(value+" for victim")
                # check of prev command includes kite
                elif "kite" in prev:
                    rospy.wait_for_service("detector")
                    detector_goal = "Did not work!"
                    try:
                        print "testedadr123789"
                        detector = rospy.ServiceProxy("detector",text_parser)
                        resp1 = detector("kite")
                        detector_goal = resp1.result
                    except rospy.ServiceException, e:
                        print"Service call failed: %s"%e
                    if detector_goal == "YES":
                        publisher.publish("Kite already found. Continue searching, yes or no?")
                        call_transparency_logging(prev, "no","", "kite", "yes")
                        return "nix"
                    else:
                        call_second_server(value+" for kite")
        else:
            publisher.publish("Please give a new instruction!")
            return "nix"

def check_other_cmds(value, prev):
    if "victim" in value:
        rospy.wait_for_service("detector")
        detected = "Did not work!"
        try:
            detector = rospy.ServiceProxy("detector",text_parser)
            resp1 = detector("victim")
            detected = resp1.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
        if detected == "YES":
            publisher.publish(value)
            call_transparency_logging(value, "yes","", "victim", "yes")
            call_second_server(value)
        else:
            publisher.publish("Victim not found yet!")
            call_transparency_logging(value, "no","", "victim", "no")
            return "nix"
    elif "kite" in value:
        rospy.wait_for_service("detector")
        detected = "Did not work!"
        try:
            #  print "tsssssssssssssssssssesteradsad123"
            detector = rospy.ServiceProxy("detector",text_parser)
            resp1 = detector("kite")
            #prev = req.goal
            detected = resp1.result
        except rospy.ServiceException, e:
            print"Service call failed: %s"%e
 
        if detected == "YES":
            publisher.publish(value)
            call_transparency_logging(value, "yes","", "kite", "yes")
            call_second_server(value)
        else:
            publisher.publish("Kite not found yet!")
            call_transparency_logging(value, "no","", "kite", "no")
            return "nix"
            
def call_main_server(req):
    global saver
    global prev_command
    print "call main server"
    serv_checker = checking_agent(req.goal)
    # if agent not capable
    print "checking the agent with: "
    print serv_checker
    if serv_checker == "NIENTE":
        call_transparency_logging(req.goal, "niente","" , "", "")
        return "Waiting!"
    elif serv_checker == "BRAVO" or serv_checker == "NOCOMMAND":
        # if continue command- yes and prev_command is assigned and not yes
        if req.goal == "yes" or req.goal == "no":
            check_yes_no_command(req.goal, prev_command)
        elif "search" in req.goal and "victim" in req.goal:
            prev_command = req.goal
            check_search_command(req.goal, "")
        elif "search" in req.goal and "kite" in req.goal:
            prev_command = req.goal
            check_search_command(req.goal, "")
        elif "search" in req.goal:
            check_search_command(req.goal, prev_command)
        elif "victim" in req.goal or "kite" in req.goal:
            check_other_cmds(req.goal, "")
        else:
            publisher.publish(req.goal)
            call_second_server(req.goal)
    else:
        return "did not work"
            
        
 
def start_main_server():
    global pub
    global pub_speaker
    global publisher
    rospy.init_node("start_main_server")
    pub = rospy.Publisher('/internal_output', Desig, queue_size=10)
    pub_speaker = rospy.Publisher('/speaker_on', String, queue_size=10)
    publisher = rospy.Publisher('display_command', String, queue_size=10)
    #rospy.Subscriber("/recognizer/output", String, call_main_server)
    s = rospy.Service("main_server", text_parser, call_main_server)
    print "Main server is up and waiting for speech!"
    rospy.spin()



if __name__ == "__main__":
    start_main_server()
