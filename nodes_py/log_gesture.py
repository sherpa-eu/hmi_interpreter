#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
import rospy
import time
import sys
import os, sys
import os.path
import random
from std_msgs.msg import String
import math
import tf
import rospkg
import time
from visualization_msgs.msg import *
from interactive_markers.interactive_marker_server import *
from geometry_msgs.msg import Pose

inFile="log_gesture.owl"
opener=''
rospack = rospkg.RosPack()
path =  rospack.get_path('hmi_interpreter')+'/nodes_py'+'/logfiles'
pointing=''

def callGesture(req):
    global opener
    global pointing
    act = req.action.data
    pointer = req.pointing
    with open(path+"/"+inFile,'r') as i:
        lines = i.readlines()
    outFile = inFile
    end2 = rospy.Time.from_sec(time.time()) #rospy.Time.now()
    t = end2.to_sec()
    end = t
    value = str(t)
    with open(path+"/"+outFile,'w') as o:
        for line in lines:
            if line == "</rdf:RDF>\n":
                if act == "human":
                    pointing=""
                    val = str(random.getrandbits(32))
                    o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#GestureReasoning_"+val+"\">\n"
                            "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#GestureReasoning\"/>\n"
                            "<knowrob:checkIfPointed rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+"No-Pointing"+"</knowrob:checkIfPointed>\n"
                            "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:quaternion rdf:datatype=\"&xsd;string\">"+str(pointer.pose.orientation.x)+" "+str(pointer.pose.orientation.y)+" "+str(pointer.pose.orientation.z)+" "+str(pointer.pose.orientation.w)+"</knowrob:quaternion>\n"
                            "<knowrob:translation rdf:datatype=\"&xsd;string\">"+str(pointer.pose.position.x)+" "+str(pointer.pose.position.y)+" "+str(pointer.pose.position.z)+"</knowrob:translation>\n"
                            "</owl:NamedIndividual>\n\n"+line)
                elif act == "pointing":
                    val = str(random.getrandbits(32))
                    if pointing == "":
                        pointing = str(random.getrandbits(8))
                        o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#GestureReasoning_"+val+"\">\n"
                                "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#GestureReasoning\"/>\n"
                                "<knowrob:checkIfPointed rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+"Pointing"+"</knowrob:checkIfPointed>\n"
                                "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                                "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                                "<knowrob:relatedPointer rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+pointing+"</knowrob:relatedPointer>\n"
                                "<knowrob:quaternion rdf:datatype=\"&xsd;string\">"+str(pointer.pose.orientation.x)+" "+str(pointer.pose.orientation.y)+" "+str(pointer.pose.orientation.z)+" "+str(pointer.pose.orientation.w)+"</knowrob:quaternion>\n"
                                "<knowrob:translation rdf:datatype=\"&xsd;string\">"+str(pointer.pose.position.x)+" "+str(pointer.pose.position.y)+" "+str(pointer.pose.position.z)+"</knowrob:translation>\n"
                                "</owl:NamedIndividual>\n\n"+line)
                    else:
                       o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#GestureReasoning_"+val+"\">\n"
                                "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#GestureReasoning\"/>\n"  
                               "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                               "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                               "<knowrob:relatedPointer rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+pointing+"</knowrob:relatedPointer>\n"
                               "<knowrob:quaternion rdf:datatype=\"&xsd;string\">"+str(pointer.pose.orientation.x)+" "+str(pointer.pose.orientation.y)+" "+str(pointer.pose.orientation.z)+" "+str(pointer.pose.orientation.w)+"</knowrob:quaternion>\n"
                               "<knowrob:translation rdf:datatype=\"&xsd;string\">"+str(pointer.pose.position.x)+" "+str(pointer.pose.position.y)+" "+str(pointer.pose.position.z)+"</knowrob:translation>\n"
                               "</owl:NamedIndividual>\n\n"+line)
                else:
                    pointing=""
                    val = str(random.getrandbits(32))
                    o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#GestureReasoning_"+val+"\">\n"
                            "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#GestureReasoning\"/>\n"
                            "<knowrob:clickOnObject rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+act+"</knowrob:clickOnObject>\n"
                            "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:quaternion rdf:datatype=\"&xsd;string\">"+str(pointer.pose.orientation.x)+" "+str(pointer.pose.orientation.y)+" "+str(pointer.pose.orientation.z)+" "+str(pointer.pose.orientation.w)+"</knowrob:quaternion>\n"
                            "<knowrob:translation rdf:datatype=\"&xsd;string\">"+str(pointer.pose.position.x)+" "+str(pointer.pose.position.y)+" "+str(pointer.pose.position.z)+"</knowrob:translation>\n"
                            "</owl:NamedIndividual>\n\n"+line)
            else:
                o.write(line)
    geom = Pose()
    return pointerResponse(geom)

def create_file():
    global opener
    global inFile
    global path
    print "createFile"
    if os.path.exists(path):
        print "directory already exist"
    else:
        os.mkdir(path, 0755)
    
    if os.path.isfile(path+"/"+inFile):
        value= random.getrandbits(16)
        inFile="log_gesture_"+str(value)+".owl"

    opener = open(path+"/"+inFile,'w')
    opener.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
                 "<!DOCTYPE rdf:RDF[\n" 
                 "<!ENTITY rdf \"http://www.w3.org/1999/02/22-rdf-syntax-ns\">\n"
                 "<!ENTITY rdfs \"http://www.w3.org/2000/01/rdf-schema\">\n"
                 "<!ENTITY owl \"http://www.w3.org/2002/07/owl\">\n"
                 "<!ENTITY xsd \"http://www.w3.org/2001/XMLSchema#\">\n"
                 "<!ENTITY knowrob \"http://knowrob.org/kb/knowrob.owl#\">\n"
                 "<!ENTITY log \"http://knowrob.org/kb/unreal_log.owl#\">\n"
                 "<!ENTITY u-map \"http://knowrob.org/kb/u_map.owl#\">\n"
                 "]>\n"
                 "<rdf:RDF xmlns:computable=\"http://knowrob.org/kb/computable.owl#\" xmlns:swrl=\"http://www.w3.org/2003/11/swrl#\" xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\" xmlns:owl=\"http://www.w3.org/2002/07/owl#\" xmlns:knowrob=\"http://knowrob.org/kb/knowrob.owl#\" xmlns:u-map=\"http://knowrob.org/kb/u_map.owl#\" xml:base=\"http://knowrob.org/kb/u_map.owl#\">\n"
	"<!--Ontologies-->\n"
	"<owl:Ontology rdf:about=\"http://knowrob.org/kb/unreal_log.owl\">\n"
                 "<owl:imports rdf:resource=\"package://knowrob_common/owl/knowrob.owl\"/>\n"
		"<!--owl:imports rdf:resource=\"package://knowrob_common/owl/sherpa.owl\"/-->\n"
	"</owl:Ontology>\n"
	"<!--Property Definitions-->\n"
	"<owl:ObjectProperty rdf:about=\"&knowrob;taskContext\"/>\n"
	"<owl:ObjectProperty rdf:about=\"&knowrob;taskSuccess\"/>\n"
	"<owl:ObjectProperty rdf:about=\"&knowrob;startTime\"/>\n"
	"<owl:ObjectProperty rdf:about=\"&knowrob;endTime\"/>\n"
	"<owl:ObjectProperty rdf:about=\"&knowrob;experiment\"/>\n"
	"<owl:ObjectProperty rdf:about=\"&knowrob;clickOnObject\"/>\n"
        "<owl:ObjectProperty rdf:about=\"&knowrob;checkIfPointed\"/>\n"
        "<owl:ObjectProperty rdf:about=\"&knowrob;relatedPointer\"/>\n"
	"<!--Class Definitions-->\n"
	"<owl:Class rdf:about=\"&knowrob;GraspingSomething\"/>\n"
                "<!--Class Definitions-->\n"
                 "<owl:Class rdf:about=\"&knowrob;CRAMAction\"/>\n"
                 "<owl:Class rdf:about=\"&knowrob;GestureReasoning\">\n"
                 "<rdfs:subClassOf rdf:resource=\"http://knowrob.org/kb/knowrob.owl#CRAMAction\"/>\n"
                 "</owl:Class>\n\n"
	"<!--Event Individuals-->\n"
	"<!--Object Individuals-->\n"
	"<owl:NamedIndividual rdf:about=\"&log;timepoint_0.0\">\n"
		"<rdf:type rdf:resource=\"&knowrob;TimePoint\"/>\n"
	"</owl:NamedIndividual>\n\n"
                 "</rdf:RDF>\n")
    opener.close()

def log_gesture():
    create_file()
    rospy.init_node("log_gesture")
    s = rospy.Service("/logging_gesture", pointer, callGesture)
    print "Logging gesture is ready to log timepoints"
    rospy.spin()

if __name__== "__main__":
    log_gesture()
