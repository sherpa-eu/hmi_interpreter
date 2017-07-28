#!/usr/bin/env python

from hmi_interpreter.srv import *
from hmi_interpreter.msg import *
import rospy
import time
import rospkg
from subprocess import Popen
import sys
import os, sys
import os.path
import random
from std_msgs.msg import String
import math
import tf
import time
from visualization_msgs.msg import *
from interactive_markers.interactive_marker_server import *

inFile="reasoning_algo.owl"
opener=''
rospack=''
rospack = rospkg.RosPack()
path = rospack.get_path('hmi_interpreter')+'/nodes_py'+'/logfiles'


def call_reasoner(req):
    global opener
    wert = req.data
    sel = req.selected
    pos = req.position
    viewpoint = req.viewpoint
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
                if pos == "final":
                    val = str(random.getrandbits(32))
                    val2 = str(random.getrandbits(64))
                    o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#ObjectReasoning_"+val+"\">\n"
                            "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#ObjectReasoning\"/>\n"
                            "<knowrob:containsInformation rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+wert+"</knowrob:containsInformation>\n"
                            "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:selectedFinalObject rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+wert+"\"/>\n"
                            "<knowrob:setViewpoint rdf:resource=\"http://knowrob.org/kb/unreal.log#"+viewpoint+"\"/>\n"
                            "<knowrob:entityInCommand rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+sel.lower()+"\"/>\n"
                            "</owl:NamedIndividual>\n\n"+line)
                elif pos == "infront":
                    val = str(random.getrandbits(32))
                    val2 = str(random.getrandbits(64))
                    o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#ObjectReasoning_"+val+"\">\n"
                            "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#ObjectReasoning\"/>\n"
                            "<knowrob:containsInformation rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+wert+"</knowrob:containsInformation>\n"
                            "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:selectedObject rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+pos+"\"/>\n"
                            "<knowrob:setViewpoint rdf:resource=\"http://knowrob.org/kb/unreal.log#"+viewpoint+"\"/>\n"
                            "<knowrob:entityInCommand rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+sel.lower()+"\"/>\n"
                            "</owl:NamedIndividual>\n\n"+line)
                elif pos == "all":
                    val = str(random.getrandbits(32))
                    val2 = str(random.getrandbits(64))
                    o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#ObjectReasoning_"+val+"\">\n"
                            "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#ObjectReasoning\"/>\n"
                            "<knowrob:containsInformation rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+wert+"</knowrob:containsInformation>\n"
                            "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:selectedObject rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+pos+"\"/>\n"
                            "<knowrob:setViewpoint rdf:resource=\"http://knowrob.org/kb/unreal.log#"+viewpoint+"\"/>\n"
                            "<knowrob:entityInCommand rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+sel.lower()+"\"/>\n"
                            "</owl:NamedIndividual>\n\n"+line)
                else:
                    val = str(random.getrandbits(32))
                    val2 = str(random.getrandbits(64))
                    o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#ObjectReasoning_"+val+"\">\n"
                            "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#ObjectReasoning\"/>\n"
                            "<knowrob:containsInformation rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+wert+"</knowrob:containsInformation>\n"
                            "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                            "<knowrob:selectedObject rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+pos+"\"/>\n"
                            "<knowrob:setViewpoint rdf:resource=\"http://knowrob.org/kb/unreal.log#"+viewpoint+"\"/>\n"
                            "<knowrob:entityInCommand rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#"+sel.lower()+"\"/>\n"
                            "</owl:NamedIndividual>\n\n"+line)


            else:
                o.write(line)

    return reasoning_algoResponse("reasoning_algo stored")

def create_file():
    global opener
    global inFile
    global path
    if os.path.exists(path):
        print "directory already exist"
    else:
        os.mkdir(path, 0755)
    
    if os.path.isfile(path+"/"+inFile):
        value= random.getrandbits(16)
        inFile="reasoning_algo_"+str(value)+".owl"

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
                 "]>\n\n"
                 "<rdf:RDF xmlns:computable=\"http://knowrob.org/kb/computable.owl#\" xmlns:swrl=\"http://www.w3.org/2003/11/swrl#\" xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\" xmlns:owl=\"http://www.w3.org/2002/07/owl#\" xmlns:knowrob=\"http://knowrob.org/kb/knowrob.owl#\" xmlns:u-map=\"http://knowrob.org/kb/u_map.owl#\" xml:base=\"http://knowrob.org/kb/u_map.owl#\">\n\n"
	"<!--Ontologies-->\n"
	"<owl:Ontology rdf:about=\"http://knowrob.org/kb/unreal_log.owl\">\n"
                 "<owl:imports rdf:resource=\"package://knowrob_common/owl/knowrob.owl\"/>\n"
		"<!--owl:imports rdf:resource=\"package://knowrob_common/owl/sherpa.owl\"/-->\n"
                 "</owl:Ontology>\n\n"
                 "<!--Property Definitions-->\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;taskContext\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;taskSuccess\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;startTime\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;endTime\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;experiment\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;entityInCommand\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;selectedObject\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;selectedFinalObject\"/>\n"
                 "<owl:ObjectProperty rdf:about=\"&knowrob;selectedObject\"/>\n\n"
                 "<!--Class Definitions-->\n"
                 "<owl:Class rdf:about=\"&knowrob;CRAMAction\"/>\n"
                 "<owl:Class rdf:about=\"&knowrob;ObjectReasoning\">\n"
                 "<rdfs:subClassOf rdf:resource=\"http://knowrob.org/kb/knowrob.owl#CRAMAction\"/>\n"
                 "</owl:Class>\n\n"
                 "<!--Event Individuals-->\n"
                 "<owl:NamedIndividual rdf:about=\"&log;timepoint_0.0\">\n"
                 "<rdf:type rdf:resource=\"&knowrob;TimePoint\"/>\n"
                 "</owl:NamedIndividual>\n"
                 "</rdf:RDF>\n")
    opener.close()


def main_output():
    create_file()
    rospy.init_node("reasoning_output_node")
    s = rospy.Service("store_reasoning_output", reasoning_algo, call_reasoner)
    print "Wait for reasoning output to log it"
    rospy.spin()

if __name__== "__main__":
    main_output()
