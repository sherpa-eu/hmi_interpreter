#! /usr/bin/env python

import rospy
from random import randint
from hmi_interpreter.srv import *
from hmi_interpreter.msg import LogInfo
from sherpa_msgs.msg import LoggedRDFEntry
import sherpa_msgs
import random
import time
import actionlib
import string


rospy.init_node('hmi_logging_server_py') 
client = actionlib.SimpleActionClient('/ue_semlog/LogEvent',sherpa_msgs.msg.LogEventAction)
print "ROS Node started"

def logging_cmd(req):
    print "modu"
    msg = LoggedRDFEntry()    

    msgs = []
    print "modu1"
    if req.goal.agent == "blue_wasp":
        agent="SherpaWaspBlue_ILQN"
    elif req.goal.agent == "donkey":
        agent="SherpaDonkey_ETJM"
    elif req.goal.agent == "red_wasp":
        agent="SherpaWaspRed_H9cB"
    elif req.goal.agent == "hawk":
        agent="SherpaHawk_POdy"
    print "modu3"
    
    print "teeest123"
    
    num =''.join(random.sample((string.ascii_uppercase+string.digits),6))
    name="http://knowrob.org/kb/unreal_log.owl#Communicating"#_"+num
    name_id_flag=randint(0,9)
    types="http://knowrob.org/kb/knowrob.owl#Communicating"
    now = req.goal.timer
    end = rospy.Time.now()
    print "und"
    print end
    msg.property_name="knowrob:startTime"
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#timepoint_"+now
    msg.use_resource=True
    msgs.append(msg)
    msg = LoggedRDFEntry()
    msg.property_name="knowrob:endTime"
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#timepoint_"+str(end)
    msg.use_resource=True
    msgs.append(msg)
    msg = LoggedRDFEntry()
    msg.property_name="knowrob:communicationToken"
    msg.rdf_datatype="http://www.w3.org/2001/XMLSchema#string"
    msg.value=req.goal.cmd
    msgs.append(msg)
    msg = LoggedRDFEntry()
    msg.property_name="knowrob:communicatorOfInfo"
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#BusyGenius_2PCw9"
    msg.use_resource=True
    msgs.append(msg)
    msg = LoggedRDFEntry()
    msg.property_name="knowrob:infoCommunicatedTo"
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#"+agent
    msg.use_resource=True
    msgs.append(msg)
    msg = LoggedRDFEntry()  
    #goal = sherpa_msgs.msg.MoveToGoal(pose)
    goal = sherpa_msgs.msg.LogEventGoal(name, name_id_flag, types, msgs)
    print "sending goal"
    client.send_goal(goal)
    print goal
    print "waiting result"
    client.wait_for_result()
    print client.get_result()
    print("Logging is working!")
    return log_infoResponse("done")

def start_bg_logs():
    print "testing start_bg_logs"
    s = rospy.Service('start_bg_logging', log_info, logging_cmd)
    print "Waiting for logger!"
    rospy.spin()    


if __name__ == '__main__':
    start_bg_logs()