#! /usr/bin/env python

import rospy
from hmi_interpreter.srv import *
from sherpa_msgs.msg import LoggedRDFEntry
from hmi_interpreter.msg import LogInfo
import random
import time
import actionlib
import string

# req.name "http://knowrob.org/kb/unreal_log.owl#UnrealExperiment_q9PX"
# req.type "http://knowrob.org/kb/knowrob.owl#UnrealExperiment"
# 
def logging_cmd(req):
    msg = LoggedRDFEntry()
    msgs = []
    if req.goal.agent == "blue_wasp":
        agent="SherpaWaspBlue_ILQN"
    elif req.goal.agent == "donkey":
        agent="SherpaDonkey_ETJM"
    elif req.goal.agent == "red_wasp":
        agent="SherpaWaspRed_H9cB"
    elif req.goal.agent == "hawk":
        agent="SherpaHawk_POdy"

  #  client = actionlib.SimpleActionClient('Logger',sherpa_msgs.msg.LogEventGoal)
  #  client.wait_for_server()
    num =''.join(random.sample((string.ascii_uppercase+string.digits),6))
    name="http://knowrob.org/kb/unreal_log.owl#SpokenCommunicating_"+num
    type="http://knowrob.org/kb/knowrob.owl#SpokenCommunicating"
    now = req.goal.timer
    end = rospy.Time.now()
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#timepoint_"+now
    msgs.append(msg)
    msg = LoggedRDFEntry()
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#timepoint_"+str(end)
    msgs.append(msg)
    msg = LoggedRDFEntry()
    msg.rdf_datatype="http://www.w3.org/2001/XMLSchema#string"
    msg.value=req.goal.cmd
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#BusyGenius_2PCw9"
    msgs.append(msg)
    msg = LoggedRDFEntry()
    msg.rdf_resource="http://knowrob.org/kb/unreal_log.owl#"+agent
    msgs.append(msg)
    msg = LoggedRDFEntry()
    print msgs
  #  goal = sherpa_msgs.msg.LogEventGoal(name, type, msgs)
   # client.send_goal(goal)
  #  client.wait_for_result()
 #   print client.get_result()
    print("Logging is working!")
    return log_infoResponse("done")

def start_bg_logs():
    rospy.init_node('hmi_logging_server_py') 
    s = rospy.Service('start_bg_logging', log_info, logging_cmd)
    print "Waiting for logger!"
    rospy.spin()
    


if __name__ == '__main__':
    start_bg_logs()
