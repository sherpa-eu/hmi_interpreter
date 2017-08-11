#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError 
import cv2
from std_msgs.msg import String
import rospkg
import time
import sys
import os, sys
import os.path
import random
from hmi_interpreter.srv import *

bridge = CvBridge()
rospack = rospkg.RosPack()
path =  rospack.get_path('hmi_interpreter')+'/nodes_py'+'/logfiles'+'/imgs'
log_path =  rospack.get_path('hmi_interpreter')+'/nodes_py'+'/logfiles'
inFile="store_imgs.owl"
opener=''



def call_image_storing(kette):
    global opener
    
    name = kette

    with open(log_path+"/"+inFile,'r') as i:
        lines = i.readlines()
    outFile = inFile
    end2 = rospy.Time.from_sec(time.time()) #rospy.Time.now()
    t = end2.to_sec()
    end = t
    value = str(t)
  
    with open(log_path+"/"+outFile,'w') as o:
        for line in lines:
            if line == "</rdf:RDF>\n":
                val = str(random.getrandbits(32))
                o.write("<owl:NamedIndividual rdf:about=\"http://knowrob.org/kb/unreal_log.owl#ImageVisualization_"+val+"\">\n"
                        "<rdf:type rdf:resource=\"http://knowrob.org/kb/knowrob.owl#ImageVisualization\"/>\n"
                        "<knowrob:imageName rdf:datatype=\"http://www.w3.org/2001/XMLSchema#string\">"+name+"</knowrob:imageName>\n"
                    "<knowrob:startTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                        "<knowrob:endTime rdf:resource=\"http://knowrob.org/kb/unreal_log.owl#timepoint_"+value+"\"/>\n"
                        "</owl:NamedIndividual>\n\n"+line)
            else:
                o.write(line)



def image_callback(msg):
    print("Received an image!")
    try:
        cv2_img= bridge.imgmsg_to_cv2(msg,"bgr8")
        val = str(random.getrandbits(16))
        tmp = 'camera_image_'+val+'.jpeg'
        call_image_storing(tmp)
        cv2.imwrite(path+'/'+tmp, cv2_img)
    except CvBridgeError, e:
        print(e)

def call_callback(kette):
    print("Received Command")
    indexy = 0
    indexi = 0
    name = kette.data
    val = str(random.getrandbits(16))
    if name == "TAKE PICTURE" or name is "FOUND KITE" or name is "FOUND VICTIM":
        tmp = 'camera_image_'+val
        rospy.wait_for_service("store_image")
        try: 
            store_image = rospy.ServiceProxy("store_image", text_parser)
            resp1 = store_image(tmp)
            result = resp1.result
            call_image_storing(tmp+'.jpg')
            return result
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        

def create_file():
    global opener
    global inFile
    global path
    print "createFiles"
    if os.path.exists(log_path):
        print "directory already exist"
    else:
        os.mkdir(log_path, 0755)

    if os.path.exists(path):
        print "directory already exist"
    else:
        os.mkdir(path, 0755)


    if os.path.isfile(log_path+"/"+inFile):
        value= random.getrandbits(16)
        inFile="store_imgs_"+str(value)+".owl"

    opener = open(log_path+"/"+inFile,'w')
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
	"<owl:ObjectProperty rdf:about=\"&knowrob;imageName\"/>\n\n"
                "<!--Class Definitions-->\n"
                 "<owl:Class rdf:about=\"&knowrob;CRAMAction\"/>\n"
                 "<owl:Class rdf:about=\"&knowrob;ImageVisualization\">\n"
                 "<rdfs:subClassOf rdf:resource=\"http://knowrob.org/kb/knowrob.owl#CRAMAction\"/>\n"
                 "</owl:Class>\n\n"
	"<!--Object Individuals-->\n"
	"<owl:NamedIndividual rdf:about=\"&log;timepoint_0.0\">\n"
		"<rdf:type rdf:resource=\"&knowrob;TimePoint\"/>\n"
	"</owl:NamedIndividual>\n\n"
                 "</rdf:RDF>\n")
    opener.close()


    

def main():
    rospy.init_node('store_imgs')
    wait_for_topic = "/internal/recognizer/output"
    rospy.Subscriber(wait_for_topic,String,call_callback)
    rospy.spin()


if __name__ =='__main__':
    create_file()
    main()
