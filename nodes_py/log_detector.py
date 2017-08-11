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

inFile="transparency_logging.owl"
opener=''
rospack = rospkg.RosPack()
path =  rospack.get_path('hmi_interpreter')+'/nodes_py'+'/logfiles'

    
def callDetection(req):
    global opener
    command=req.command.data
    executable=req.executable.data
    agent=req.agentname.data
    neededCap=req.neededCap.data
    givenCap=req.givenCap.data
    objName = req.neededObj.data
    found = req.foundObj.data
    
  
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
                val = str(random.getrandbits(32))
                o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#AgentCommunication_"+val+"\">\n"
                        "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#AgentCommunication\"/>\n"
                        "<knowrob:agentAssigned rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+agent+"</knowrob:agentAssigned>\n"
                        "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                        "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                        "<knowrob:taskInformation rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+command+"</knowrob:taskInformation>\n")
                if executable == "yes":
                    o.write("<knowrob:taskExecutable rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+executable+"</knowrob:taskExecutable>\n"
                            "</owl:NamedIndividual>\n\n"+line)
                elif executable == "niente":
                    o.write("<knowrob:taskExecutable rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+"no"+"</knowrob:taskExecutable>\n"
                            "<knowrob:checkReason rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#Capabilities\"/>\n"
                            "<knowrob:hasCap rdf:resource=\""+givenCap+"\"/>\n"
                            "<knowrob:needCap rdf:resource=\""+neededCap+"\"/>\n"
                            "</owl:NamedIndividual>\n\n"+line)
                elif executable == "no":
                    o.write("<knowrob:taskExecutable rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+executable+"</knowrob:taskExecutable>\n")
                    if found == "yes":
                        o.write("<knowrob:objectName rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+objName+"</knowrob:objectName>\n"
                                "<knowrob:checkReason rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#FoundObject\"/>\n"
                                "<knowrob:objectAvailable rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+"object-already-found"+"</knowrob:objectAvailable>\n"
                                "</owl:NamedIndividual>\n\n"+line)
                    else:
                        o.write("<knowrob:objectName rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+objName+"</knowrob:objectName>\n"
                                "<knowrob:checkReason rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#NoObjectFound\"/>\n"
                                "<knowrob:objectAvailable rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+"object-not-found"+"</knowrob:objectAvailable>\n"
                                "</owl:NamedIndividual>\n\n"+line)
            else:
                o.write(line)

    result = String()
    result.data="Logging successful"
    return logging_detectorResponse(result)


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
        inFile="transparency_logging_"+str(value)+".owl"

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
        "<owl:ObjectProperty rdf:about=\"&knowrob;needCap\"/>\n"
        "<owl:ObjectProperty rdf:about=\"&knowrob;checkReason\"/>\n"
        "<owl:ObjectProperty rdf:about=\"&knowrob;hasCap\"/>\n"
        "<owl:ObjectProperty rdf:about=\"&knowrob;availableCapability\"/>\n"
	"<!--Class Definitions-->\n"
	"<owl:Class rdf:about=\"&knowrob;GraspingSomething\"/>\n"
                 "<owl:Class rdf:about=\"&knowrob;CRAMAction\"/>\n"
                 "<owl:Class rdf:about=\"&knowrob;AgentCommunication\">\n"
                 "<rdfs:subClassOf rdf:resource=\"http://knowrob.org/kb/knowrob.owl#CRAMAction\"/>\n"
                 "</owl:Class>\n\n"
	"<!--Event Individuals-->\n"
	"<!--Object Individuals-->\n"
	"<owl:NamedIndividual rdf:about=\"&log;timepoint_0.0\">\n"
		"<rdf:type rdf:resource=\"&knowrob;TimePoint\"/>\n"
	"</owl:NamedIndividual>\n\n"
                 "</rdf:RDF>\n")
    opener.close()
    print "ok close"

def log_detector():
    create_file()
    rospy.init_node("log_detector")
    s = rospy.Service("/logging_detection", logging_detector, callDetection)
    print "Logging transparency of communication"
    rospy.spin()

if __name__== "__main__":
    log_detector()
