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
def create_hmi_msgs(goal, agent, viewpoint, pose, openEase):
    print "create_hmi_msgs"
    global desigs
    print "agent"
    print agent
    print goal
    print "pose"
    print pose
    desig = Desig()
    desigs = []
    goal = goal.split(" 0 ")
    propkey = Propkey()
    propkey2 = Propkey()
    propkeys = []
    point = Point()
    if len(goal) == 1:
        goal = goal[0].split(" 1 ")
        if len(goal) == 1:                                 #Go to tree
            goal = goal[0].split(" ")
            desig.action_type.data = goal[0]
            desig.actor.data = agent
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
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
            desigs.append(desig)
        else:
            goal1 = goal[0].split(" ")                    #Go to tree to rock
            desig.action_type.data = goal1[0]
            desig.actor.data = agent
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
          
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
            desigs.append(desig)
            desig = Desig()
    else:   
        goal1 = goal[0].split(" 1 ")
        if len(goal1) == 1:  
            goal1 = goal1[0].split(" ")                                 #Go to tree
            desig.action_type.data = goal1[0]
            desig.actor.data = agent
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
        
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
            desigs.append(desig)
            desig = Desig()
        else:
            goal3 = goal1[0].split(" ")                                             #Go right to tree
            desig.action_type.data = goal3[0]
            desig.actor.data = agent
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
         
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
            desigs.append(desig)
            desig = Desig()

        goal2 = goal[1].split(" 1 ")
        if len(goal2) == 1:                                                    #take-picture
            goal2 = goal2[0].split(" ")
            desig.action_type.data = goal2[0]
            desig.actor.data = agent
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
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
            desigs.append(desig)
            desig = Desig()
            propkeys = []
        else:                                                              #take picture to rock
            goal1 = goal2[0].split(" ")
            desig = Desig()
            propkey = Propkey()
            propkey2 = Propkey()
            propkeys = []
            desig.action_type.data = goal1[0]
            desig.actor.data = agent
            desig.instructor.data = "busy_genius"
            if viewpoint == "yes":
                desig.viewpoint.data = agent
            else:
                desig.viewpoint.data = "busy_genius"
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
            desigs.append(desig)
            desig = Desig()
    
   # print desigs
    
def call_main_server(req):
    global agent00
    # create client for ros_parser
    print "call_main_server"
    print req.goal
    rospy.wait_for_service("ros_parser")
    result = "Did not work!"
    try:
        ros_parser = rospy.ServiceProxy("ros_parser",text_parser)
        resp1 = ros_parser(req.goal)
        #print "teeest"
        result = resp1.result
        # CREATE POSE CLIENT      
        # GENERATE the CRAM CLIENT
        #return "Okay everything went well"
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
    print "ros_parser"
    print result
    rospy.wait_for_service("add_agent_name")
    agent = "Did not work!"
    try:
        add_agent_name = rospy.ServiceProxy("add_agent_name",text_parser)
        resp2 = add_agent_name("get")
        agent = resp2.result
        #create_hmi_msgs(resp1.result)
        # GENERATE the CRAM CLIENT
        #return "Okay everything went well"
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

    # agent00 = agent
    # rospy.wait_for_service("start_bg_logging")
    # bg = "Did not work!"
    # print agent00
    # try:
    #     start_bg_logging = rospy.ServiceProxy("start_bg_logging",log_info)
    #     goal = LogInfo()
    #     end2 = rospy.Time.from_sec(time.time()) rospy.Time.now()
    #     t = end2.to_sec()
    #     end = t
    #     goal.timer=str(end)
    #     goal.agent=agent00
    #     goal.cmd=req.goal
    #     resp3 = start_bg_logging(goal)
    #     bg = resp3.result
    #     create_hmi_msgs(resp1.result)
    #     GENERATE the CRAM CLIENT
    #     return "Okay everything went well"
    # except rospy.ServiceException, e:
    #     print"Service call failed: %s"%e
        
    rospy.wait_for_service("add_viewpoint")
    viewpoint = "Did not work!"
    try:
        add_viewpoint = rospy.ServiceProxy("add_viewpoint",text_parser)
        resp2 = add_viewpoint("get")
        viewpoint = resp2.result
        #create_hmi_msgs(resp1.result)
        # GENERATE the CRAM CLIENT
        #return "Okay everything went well"
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

    rospy.wait_for_service("pointing_server")
    pose = "Did not work!"
    try:
        pointing_server = rospy.ServiceProxy("pointing_server",pointer)
        print "pointing"
        string = String()
        posy = PoseStamped()
        string.data = "get"
        print "posy"
        print posy
        resp2 = pointing_server(string,posy)
        print resp2.result
        posy = resp2.result
        #create_hmi_msgs(resp1.result)
        # GENERATE the CRAM CLIENT
        #return "Okay everything went well"
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
    
    rospy.wait_for_service("add_openEase_object")
    pose = "Did not work!"
    try:
        add_openEase_object = rospy.ServiceProxy("add_openEase_object",text_parser)
        string = String()
        string.data = "get"
        resp2 = add_openEase_object("get")
        openEase = resp2.result
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e
        
    create_hmi_msgs(resp1.result, agent, viewpoint, posy,openEase)
    pub.publish(desigs[0])
    rate = rospy.Rate(20)
    print desigs[0]
    rospy.wait_for_service("service_hmi_cram")
    result = "Did not work!"
    try:
        service_hmi_cram = rospy.ServiceProxy("service_hmi_cram",HMIDesig)
        resp2 = service_hmi_cram(desigs)
        tmp = resp2.result
  
        time.sleep(5)
        pub_speaker.publish("done")
        print "main-server"
        return tmp
        #     #return "Okay everything went well"
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

 
def start_main_server():
    global pub
    global pub_speaker
    rospy.init_node("start_main_server")
    pub = rospy.Publisher('/internal_output', Desig, queue_size=10)
    pub_speaker = rospy.Publisher('/speaker_on', String, queue_size=10)
    #rospy.Subscriber("/recognizer/output", String, call_main_server)
    s = rospy.Service("main_server", text_parser, call_main_server)
    print "Main server is up and waiting for speech!"
    rospy.spin()



if __name__ == "__main__":
    start_main_server()
