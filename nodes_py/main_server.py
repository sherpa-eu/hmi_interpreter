#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
import sys

desigs = ""
pose  = ""
def create_hmi_msgs(goal, agent, pose):
    global desigs
    print agent
    print goal
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
            desig.instructor.data = "busy-genius"
            desig.viewpoint.data = "busy-genius"
            propkey.object_relation.data = goal[1]
            propkey.object.data = goal[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal[3]
            propkey.pointing_gesture.x = pose.position.x
            propkey.pointing_gesture.y = pose.position.y
            propkey.pointing_gesture.z = pose.position.z
            propkeys.append(propkey)
            propkey = Propkey()
            desig.propkeys = propkeys
            desigs.append(desig)
        else:
            goal1 = goal[0].split(" ")                    #Go to tree to rock
            desig.action_type.data = goal1[0]
            desig.actor.data = agent
            desig.instructor.data = "busy-genius"
            desig.viewpoint.data = "busy-genius"
            propkey.object_relation.data = goal1[1]
            propkey.object.data = goal1[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal1[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal1[3]
            propkey.pointing_gesture.x = pose.position.x
            propkey.pointing_gesture.y = pose.position.y
            propkey.pointing_gesture.z = pose.position.z
            propkeys.append(propkey)
            propkey = Propkey()
            goal2 = goal[1].split(" ")
            propkey.object_relation.data = goal2[0]
            propkey.object.data = goal2[3]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal2[1]
            propkey.object_num.data = "null"
            propkey.flag.data = goal2[2]
            propkey.pointing_gesture.x = pose.position.x
            propkey.pointing_gesture.y = pose.position.y
            propkey.pointing_gesture.z = pose.position.z
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
            desig.instructor.data = "busy-genius"
            desig.viewpoint.data = "busy-genius"
            propkey.object_relation.data = goal1[1]
            propkey.object.data = goal1[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal1[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal1[3]
            propkey.pointing_gesture.x = pose.position.x
            propkey.pointing_gesture.y = pose.position.y
            propkey.pointing_gesture.z = pose.position.z
            propkeys.append(propkey)
            desig.propkeys = propkeys
            desigs.append(desig)
            desig = Desig()
        else:
            goal3 = goal1[0].split(" ")                                             #Go right to tree
            desig.action_type.data = goal3[0]
            desig.actor.data = agent
            desig.instructor.data = "busy-genius"
            desig.viewpoint.data = "busy-genius"
            propkey.object_relation.data = goal3[1]
            propkey.object.data = goal3[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal3[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal3[3]
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
            propkey.pointing_gesture.x = pose.position.x
            propkey.pointing_gesture.y = pose.position.y
            propkey.pointing_gesture.z = pose.position.z
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
            desig.instructor.data = "busy-genius"
            desig.viewpoint.data = "busy-genius"
            propkey = Propkey()
            propkey.object_relation.data = goal2[1]
            propkey.object.data = goal2[4]
            propkey.object_color.data = "null"
            propkey.object_size.data = goal2[2]
            propkey.object_num.data = "null"
            propkey.flag.data = goal2[3]
            propkey.pointing_gesture.x = pose.position.x
            propkey.pointing_gesture.y = pose.position.y
            propkey.pointing_gesture.z = pose.position.z
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
            desig.instructor.data = "busy-genius"
            desig.viewpoint.data = "busy-genius"
            propkey2.object_relation.data = goal1[1]
            propkey2.object.data = goal1[4]
            propkey2.object_color.data = "null"
            propkey2.object_size.data = goal1[2]
            propkey2.object_num.data = "null"
            propkey2.flag.data = goal1[3]
            propkey2.pointing_gesture.x = pose.position.x
            propkey2.pointing_gesture.y = pose.position.y
            propkey2.pointing_gesture.z = pose.position.z
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
            propkey2.pointing_gesture.x = pose.position.x
            propkey2.pointing_gesture.y = pose.position.y
            propkey2.pointing_gesture.z = pose.position.z
            propkeys.append(propkey2)
            propkeys.reverse()
            desig.propkeys = propkeys
            desigs.append(desig)
            desig = Desig()
    
   # print desigs
    
def call_main_server(req):
    # create client for ros_parser
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

    rospy.wait_for_service("pointing_server")
    pose = "Did not work!"
    try:
        pointing_server = rospy.ServiceProxy("pointing_server",pointer)
        print "get"
        string = String()
        posy = Pose()
        string.data = "get"
        resp2 = pointing_server(string,posy)
        pose = resp2.result
        #create_hmi_msgs(resp1.result)
        # GENERATE the CRAM CLIENT
        #return "Okay everything went well"
    except rospy.ServiceException, e:
        print"Service call failed: %s"%e

    create_hmi_msgs(resp1.result, agent, pose)
    print desigs
  
    # rospy.wait_for_service("service_cram_reasoning")
    # result = "Did not work!"
    # try:
    #     service_cram_reasoning = rospy.ServiceProxy("service_cram_reasoning",HMIDesig)
    #     resp2 = service_cram_reasoning(desigs)
    #     return resp2.result
    #     #return "Okay everything went well"
    # except rospy.ServiceException, e:
    #     print"Service call failed: %s"%e


#     return text_parserResponse(req.goal)

#def call_main_server(data):
 #   rospy.loginfo("Main_server heard %s", data.data)
    # server speechToText
    # client ros_parser
    # create_hmi_msgs

# def check_pose_client():
#     rospy.wait_for_service("pointing_gesture")
#     try:
#        pointing_gesture = rospy.ServiceProxy("pointing_gesture",--pointing-gesture-service)
#        resp1 = pointing_gesture(--string is asking -- )
#        print resp1.sum -- getting the resuklt and storing in pose
#        pose = resp1.sum
#     except rospy.ServiceException, e:
#         print "Service call failed: %s"%e

def start_main_server():
    rospy.init_node("start_main_server")
    #rospy.Subscriber("/recognizer/output", String, call_main_server)
    s = rospy.Service("main_server", text_parser, call_main_server)
    print "Main server is up and waiting for speech!"
    rospy.spin()



if __name__ == "__main__":
    start_main_server()
