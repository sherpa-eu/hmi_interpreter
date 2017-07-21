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

inFile="all_timepoints.owl"
opener=''
rospack = rospkg.RosPack()
path =  rospack.get_path('hmi_interpreter')+'/nodes_py'+'/logfiles'


def log_timepoints():
    global opener
    print log_timepoints
    with open(path+"/"+inFile,'r') as i:
        lines = i.readlines()
    print log_timepoints
    outFile = inFile
    end2 = rospy.Time.from_sec(time.time()) #rospy.Time.now()
    t = end2.to_sec()
    end = t
    value = str(t)
    with open(path+"/"+outFile,'w') as o:
        for line in lines:
            if line == "</rdf:RDF>\n":
                o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/knowrob.owl#timepoint_"+value+"\">\n"
                        "<rdf:type rdf:resource=\"&knowrob;TimePoint\"/>\n"
                        "</owl:NamedIndividual>\n"+line)
            else:
                o.write(line)
    
def visualizeMarker(array):
    print "visualizemarker"
    publisher = rospy.Publisher("/visualization_marker_array",MarkerArray,queue_size=10)
  #  rospy.init_node("simple_marker",anonymous=True)
    cubes = MarkerArray()
    marker = Marker()
    marker.header.frame_id = "/map"
    marker.header.stamp = rospy.Time.now()
    marker.id = random.getrandbits(16)
    marker.type = marker.CUBE
    marker.action = marker.ADD
    marker.pose.position.x = array[0]
    marker.pose.position.y = array[1]
    marker.pose.position.z = array[2]
    marker.scale.x = 6.0
    marker.scale.y = 6.0
    marker.scale.z = 3.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0
    marker.color.a = 0.7
    cubes.markers.append(marker)
    publisher.publish(cubes)
   


def callCB(req):
    print "callCB"
    listener = tf.TransformListener()
    rate = rospy.Rate(50.0)
   # index = 0
    while not rospy.is_shutdown():
        log_timepoints()
        print "sleep"
       # index = index+1
       #  rospy.sleep(1)






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
        inFile="all_timepoints_"+str(value)+".owl"

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
	"<!--Class Definitions-->\n"
	"<owl:Class rdf:about=\"&knowrob;GraspingSomething\"/>\n"
	"<!--Event Individuals-->\n"
	"<!--Object Individuals-->\n"
	"<owl:NamedIndividual rdf:about=\"&log;timepoint_0.0\">\n"
		"<rdf:type rdf:resource=\"&knowrob;TimePoint\"/>\n"
	"</owl:NamedIndividual>\n"
                 "</rdf:RDF>\n")
    opener.close()

def cram_scanned():
    create_file()
    rospy.init_node("cram_scanned")
    rospy.Subscriber("/all_timepoints_sub", String, callCB)
    print "AllTimepoints is ready to log timepoints"
    rospy.spin()

if __name__== "__main__":
    cram_scanned()
