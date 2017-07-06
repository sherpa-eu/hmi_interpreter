#!/usr/bin/env python
 
from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
from json_prolog import json_prolog
import rospy
 
result=''

def detecting(sentence):
    global result
    prolog = json_prolog.Prolog()
    if sentence == "victim":
        query = prolog.query("current_object_pose('http://knowrob.org/kb/unreal_log.owl#SherpaVictim_VAZg',A)")
        for solution in query.solutions():
            print 'Found solution. A = %s' % (solution['A'])
            s = solution['A']
        query.finish()
        if s[0] == 0 and s[1] == 0 and s[2] == 0:
            result = "NO"
        else:
            result = "YES"
    elif sentence == "kite" or sentence == "hangglider":
        query = prolog.query("current_object_pose('http://knowrob.org/kb/unreal_log.owl#SherpaHangGlider_rjI4',A)")
        for solution in query.solutions():
            print 'Found solution. A = %s' % (solution['A'])
            s = solution['A']
        query.finish()
        if s[0] == 0 and s[1] == 0 and s[2] == 0:
            result = "NO"
        else:
            result = "YES"   
    else:
        print "Object not detected"

def call_detector(req):
    print "Calling detector"
    detecting(req.goal)
    speech_output = result
    return text_parserResponse(speech_output)

def detector():
    rospy.init_node("detector_caller")
    s = rospy.Service("detector",text_parser,call_detector)
    print "Command for proofing detection of objects!"
    rospy.spin()

if __name__ == "__main__":
    detector()
